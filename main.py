import sys

# Force Python to evict page1 from cache so it re-reads the file on every rerun
if "Frontend.page1" in sys.modules:
    del sys.modules["Frontend.page1"]

from Frontend.page1 import Page1

page = Page1()
page.sidebar()
page.render()