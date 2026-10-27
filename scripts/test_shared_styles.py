"""Check shared style wiring so pages cannot silently drift apart."""

from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
from urllib.parse import urlsplit


SITE = Path(__file__).resolve().parents[1] / "static-html"


class StylesheetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stylesheets = []
        self.inline_styles = 0
        self.main_classes = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.stylesheets.append(attrs["href"])
        if tag == "style":
            self.inline_styles += 1
        if tag == "main":
            self.main_classes.extend(attrs.get("class", "").split())


class SharedStyleTests(unittest.TestCase):
    def test_all_pages_load_the_same_shared_version(self):
        versions = set()
        for page in SITE.rglob("*.html"):
            with self.subTest(page=page.name):
                parser = StylesheetParser()
                parser.feed(page.read_text(encoding="utf-8"))
                shared = [urlsplit(url) for url in parser.stylesheets
                          if urlsplit(url).path.endswith("/assets/style.css")]
                self.assertEqual(len(shared), 1)
                self.assertTrue(shared[0].query)
                versions.add(shared[0].query)
        self.assertEqual(len(versions), 1)
        imports = re.findall(r"@import url\(['\"](.+?)['\"]\)",
                             (SITE / "assets/style.css").read_text())
        self.assertEqual(len(imports), 3)
        for imported in imports:
            self.assertIn(urlsplit(imported).query, versions)

    def test_bttf_languages_share_scoped_article_styles(self):
        for language in ("en", "zh"):
            parser = StylesheetParser()
            parser.feed((SITE / f"blog/bttf-blog-{language}.html").read_text(encoding="utf-8"))
            self.assertEqual(parser.inline_styles, 0)
            self.assertIn("bttf-article", parser.main_classes)
            self.assertEqual(sum(urlsplit(url).path.endswith("/assets/blog-bttf.css")
                                 for url in parser.stylesheets), 1)


if __name__ == "__main__":
    unittest.main()
