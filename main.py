from requests import Session
from bs4 import BeautifulSoup
import re
import os
import pandas as pd
import time
import numpy as np

# %% Arguments.
# The directory to save the book.
target = 'raw/听说你喜欢我'
# The index page of the book at https://www.51shucheng.net
source = 'https://www.51shucheng.net/yanqing/tingshuonixihuanwo'
# If True, the downloading progress of chapters will be cleared. The program will overwrite from the first chapter, but
# will not delete existed chapter files.
clear_progress = False
# If True, the program will ignore `clear_progress` flag, get the table of contents, and clear the downloading progress
# of chapters, but will not delete existed chapter files.
clear_cover = False
# If True, the program will raise an error if a chapter is absent when combining all chapters to a book.
strict_compiling = True

# %% Initialize constants.
chrome_110 = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"', 'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 '
                  'Safari/537.36'
}
session = Session()
session.trust_env = False
target = os.path.abspath(target)
cover_path = os.path.join(target, 'index')
toc_path = os.path.join(target, '.toc')

# %% Check workspace.
if os.path.isfile(target):
    os.remove(target)
if not os.path.isdir(target):
    os.makedirs(target, exist_ok=True)

# %% Download basic information.
with open('data/book_prefix.tex', 'r') as f:
    cover_latex = f.read()
if (not os.path.exists(cover_path)) or (not os.path.exists(toc_path)) or clear_cover:
    cover_page = session.get(url=source, headers=chrome_110)
    if cover_page.status_code != 200:
        raise Exception(f'Fail to get the cover page. Status code: {cover_page.status_code}.')
    else:
        print('[INFO] Success to get the cover page.')
    cover_page.encoding = 'utf-8'
    cover_text = BeautifulSoup(cover_page.text, features='html.parser')
    if (not os.path.exists(cover_path)) or clear_cover:
        book_title = cover_text.find('div', {'class': 'catalog'}).h1.text
        book_author = re.sub('.*作者：', '', cover_text.find('div', {'class': 'info'}).text.strip())
        book_abstract = cover_text.find('div', {'class': 'intro'}).text
        cover_latex = cover_latex.replace(r'\title{}', r'\title{%s}' % book_title) \
            .replace(r'\author{}', r'\author{%s}' % book_author) \
            .replace('ABSTRACT', book_abstract)
        with open(cover_path, 'w', encoding='utf-8') as f:
            f.write(cover_latex)
    if (not os.path.exists(toc_path)) or clear_cover:
        chapter_list = cover_text.find('div', {'class': 'mulu-list'}).find_all('li')
        chapter_list = [[x.a.text, x.a['href']] for x in chapter_list]
        toc_df = pd.DataFrame(data=chapter_list, columns=['name', 'link'])
        toc_df['downloaded'] = None
        toc_df.to_pickle(toc_path)
    else:
        toc_df = pd.read_pickle(toc_path)
else:
    toc_df = pd.read_pickle(toc_path)

# %% Download chapters.
if clear_progress:
    toc_df['downloaded'] = None
chapters_not_downloaded = toc_df[toc_df['downloaded'].isna()].copy(deep=True)
for i, chapter in chapters_not_downloaded.iterrows():
    chapter_path = os.path.join(target, f"chapter_{i}")
    chapter_page = session.get(url=chapter['link'], headers=chrome_110)
    if chapter_page.status_code != 200:
        print(f'[Warning] Fail to download chapter {i}. Status code: {chapter_page.status_code}. Please find the'
              f'chapter at {chapter["link"]} and save it at {chapter_path}')
        print(f'[INFO]     Progress: {np.sum(toc_df["downloaded"] == 1)} errors, {np.sum(toc_df["downloaded"] == 0)} '
              f'success, {np.sum(toc_df["downloaded"].isna())} to do.')
        toc_df.loc[i, 'downloaded'] = 1
        toc_df.to_pickle(toc_path)
        continue
    chapter_page.encoding = 'utf-8'
    chapter_text = BeautifulSoup(chapter_page.text, features='html.parser')
    chapter_title = chapter_text.find('h1').text
    chapter_normal = chapter_text.find('div', {'class': 'neirong'}).text
    chapter_normal = chapter_normal.replace('\xa0', '')
    chapter_normal = re.sub('\n+', '\n\n', chapter_normal)
    with open(chapter_path, 'w', encoding='utf-8') as f:
        f.write(r'\section{' + chapter_title + '}\n')
        f.write(chapter_normal)
    toc_df.loc[i, 'downloaded'] = 0
    toc_df.to_pickle(toc_path)
    print(f'[INFO] Success to download chapter {i}. Title: {chapter_title}.')
    print(f'[INFO]     Progress: {sum(toc_df["downloaded"] == 1)} errors, {sum(toc_df["downloaded"] == 0)} success, '
          f'{sum(toc_df["downloaded"].isna())} to do.')
    time_sleep_sec = round(np.random.uniform(0.5, 1), 2)
    time.sleep(time_sleep_sec)

# %% Compiling
book = ''
print('[INFO] Start to combine chapters into one file.')
with open(cover_path, 'r', encoding='utf-8') as g:
    book += g.read()
for i in toc_df.index:
    chapter_path = os.path.join(target, f'chapter_{i}')
    try:
        with open(chapter_path, 'r', encoding='utf-8') as g:
            book += g.read()
    except FileNotFoundError:
        chapter_absent_message = f'Chapter {i} is absent. Please find it at {toc_df.loc[i, "link"]} and save ' \
                                 f'it at {chapter_path}'
        if strict_compiling:
            raise Exception(chapter_absent_message)
        else:
            print('[INFO] ' + chapter_absent_message)
with open('data/book_suffix.tex', 'r', encoding='utf-8') as f:
    book += f.read()
book_path = os.path.join(target, 'book.tex')
with open(book_path, 'w', encoding='utf-8') as f:
    f.write(book)
