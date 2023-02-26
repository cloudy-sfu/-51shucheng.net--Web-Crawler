import os
import pandas as pd

# %% Arguments.
# The directory to save the book.
target = 'raw/听说你喜欢我'

# %% Load TOC file.
target = os.path.abspath(target)
cover_path = os.path.join(target, 'index')
toc_path = os.path.join(target, '.toc')
toc_df = pd.read_pickle(toc_path)

# %% Delete cached files.
for i in toc_df.index:
    try:
        chapter_path = os.path.join(target, f'chapter_{i}')
        os.remove(chapter_path)
    except FileExistsError:
        pass
try:
    os.remove(toc_path)
except FileExistsError:
    pass
try:
    os.remove(cover_path)
except FileExistsError:
    pass
