# “51shucheng.net” Web Crawler
 Download books from "51shucheng.net" and convert to Microsoft Word

![](https://shields.io/badge/dependencies-Python_3.10-blue)
![](https://shields.io/badge/dependencies-Pandoc-blue)

# Usage

1.   Run `pip install -r requirements.txt` to install libraries. Specifically, if you do not have Pandoc, please install `pypandoc_binary` instead of `pypandoc`. See https://pypi.org/project/pypandoc/ for details.

2.   Follow the guidance of comments and set arguments in `Arguments` section of `main.py`. For example:
     ```python
     # The directory to save the book.
     target = 'raw/downloaded_book'
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
     ```

3.   Run `main.py`, you can pause at any time by pressing `Ctrl+C` (default keyboard interruption signal), and the program will resume at next run. If you want to resume from the beginning, please change `clear_progress` or `clear_cover` argument.

4.   Collect the book in format of Microsoft Word at `$target/book.docx`. If you have Microsoft Word, you can click `File | Info | Convert (Compatibility Mode)` button, and print to PDF as you want.

5.   If you're satisfied with the result, you can run `clear_cache.py` to clear caches generated when handling this book.

