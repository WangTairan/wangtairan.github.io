"""Regression checks for static resume date generation."""

from datetime import date, datetime
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest

from update_resume_date import resume_date, stamp_date


class ResumeDateTests(unittest.TestCase):
    def test_static_english_date_and_other_dates_unchanged(self):
        html = '<time>Jun 2025</time><time id="resume-updated" datetime="old">old</time>'
        rendered = stamp_date(html, date(2026, 10, 27))
        self.assertIn('<time>Jun 2025</time>', rendered)
        self.assertIn('datetime="2026-10-27">27 Oct 2026</time>', rendered)
        self.assertEqual(stamp_date(rendered, date(2026, 10, 27)), rendered)

    def test_missing_or_duplicate_marker_is_rejected(self):
        tag = '<time id="resume-updated" datetime="old">old</time>'
        for html in ("", tag + tag):
            with self.assertRaises(ValueError):
                stamp_date(html, date(2026, 10, 27))

    def test_pdf_history_not_checkout_or_unrelated_commit_date(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            pdf = root / "resume.pdf"
            def git(*args, env=None):
                return subprocess.run(
                    ["git", *args], cwd=root, env=env, check=True,
                    capture_output=True, text=True,
                )
            def commit(day):
                env = dict(os.environ, GIT_AUTHOR_DATE=day, GIT_COMMITTER_DATE=day)
                git("-c", "user.name=Date Test", "-c", "user.email=test@example.com",
                    "-c", "commit.gpgsign=false", "commit", "-qm", "test", env=env)
            git("init", "-q")
            pdf.write_bytes(b"original test PDF")
            git("add", "resume.pdf")
            commit("2026-03-02T12:00:00+00:00")
            (root / "unrelated.txt").write_text("unrelated", encoding="utf-8")
            git("add", "unrelated.txt")
            commit("2026-04-05T12:00:00+00:00")
            self.assertEqual(resume_date(root, pdf), date(2026, 3, 2))
            pdf.write_bytes(b"edited test PDF")
            changed = datetime.fromisoformat("2026-05-06T12:00:00+00:00").timestamp()
            os.utime(pdf, (changed, changed))
            self.assertEqual(resume_date(root, pdf), date(2026, 5, 6))
            git("add", "resume.pdf")
            self.assertEqual(resume_date(root, pdf), date(2026, 5, 6))


if __name__ == "__main__":
    unittest.main()
