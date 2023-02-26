# “51shucheng.net” Web Crawler

 Download books from "51shucheng.net" and convert to PDF

![](https://shields.io/badge/dependencies-Python_3.10-blue)
![](https://shields.io/badge/dependencies-XeLaTex-blue)

# Usage

1.   Run `pip install -r requirements.txt` to install libraries.
2.   Follow the guidance of comments and set arguments in `Arguments` section of `main.py` and `clear_cache.py`.
3.   Run `main.py`, you can pause at any time by pressing `Ctrl+C` (default keyboard interruption signal), and the program will resume at next run. If you want to resume from the beginning, please change `clear_progress` or `clear_cover` argument.
4.   Download [SourceHanSerifCN-Regular.ttf](https://github.com/wordshub/free-font/blob/master/assets/font/%E4%B8%AD%E6%96%87/%E6%80%9D%E6%BA%90%E5%AD%97%E4%BD%93%E7%B3%BB%E5%88%97/%E6%80%9D%E6%BA%90%E5%AE%8B%E4%BD%93/SourceHanSerifCN-Regular.ttf) and put it in any directory.
5.   Move `$target/book.tex` to the same directory as the font above, and use `XeLaTex` to compile it.
6.   If you're satisfied with the result, you can run `clear_cache.py` to clear caches generated when handling this book.

