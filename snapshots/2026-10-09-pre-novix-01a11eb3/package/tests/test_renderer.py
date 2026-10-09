"""Public, synthetic renderer regressions; no user reports or account data."""
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("renderer", ROOT / "scripts/md_to_pdf.py")
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


class RendererTests(unittest.TestCase):
    def test_default_brand_and_escaped_metadata(self):
        html = renderer.md_to_html('# 测试报告\n\n中文事实与条件。', author='作者 <测试>')
        self.assertIn('Future Clinic', html)
        self.assertIn('<title>测试报告</title>', html)
        self.assertIn('作者 &lt;测试&gt;', html)
        self.assertIn('name="author"', html)

    def test_configurable_font_is_validated(self):
        with patch.dict(os.environ, {'FUTURE_CLINIC_PDF_CJK_FONT': '/missing/font.ttf'}):
            with self.assertRaises(RuntimeError):
                renderer.resolve_pdf_cjk_font()
        self.assertTrue(renderer.BUNDLED_PDF_CJK_FONT.is_file())

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            source, output = path / 'source.md', path / 'existing.pdf'
            source.write_text('# 测试报告\n\n正文。', encoding='utf-8')
            output.write_bytes(b'existing user artifact')
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/md_to_pdf.py'), str(source), str(output)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output.read_bytes(), b'existing user artifact')


if __name__ == '__main__':
    unittest.main()
