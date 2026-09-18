#!/usr/bin/env python3
"""
Future Clinic Markdown → PDF renderer (WeasyPrint)
用法: python md_to_pdf.py input.md output.pdf [--title "报告标题"] [--author "作者"]

Dependencies: install requirements.txt in a virtual environment.
"""

import os
import re
import argparse
import html
import json
from pathlib import Path
import markdown
from fontTools.ttLib import TTFont


PDF_CJK_FONT_FAMILY = "Future Clinic PDF CJK"
BUNDLED_PDF_CJK_FONT = (
    Path(__file__).resolve().parents[1] / "assets" / "NotoSansSC[wght].ttf"
)
PDF_CJK_REQUIRED_TEXT = "中文简体报告事实解释路线条件后果改变"


def validate_pdf_cjk_font(font_path):
    """Require a glyf-based TrueType font with representative Simplified Chinese."""
    if font_path.suffix.lower() != ".ttf":
        raise RuntimeError(f"PDF CJK font must be a .ttf file: {font_path}")
    try:
        font = TTFont(str(font_path), lazy=True)
    except Exception as exc:
        raise RuntimeError(f"PDF CJK font is not a readable TrueType font: {font_path}") from exc
    try:
        if "glyf" not in font:
            raise RuntimeError(
                f"PDF CJK font must use TrueType glyf outlines, not CFF outlines: {font_path}"
            )
        cmap = font.getBestCmap() or {}
    finally:
        font.close()
    missing = [character for character in PDF_CJK_REQUIRED_TEXT if ord(character) not in cmap]
    if missing:
        raise RuntimeError(
            f"PDF CJK font lacks required Simplified Chinese glyphs {missing}: {font_path}"
        )
    return font_path.resolve()


def resolve_pdf_cjk_font():
    """Return a TrueType CJK font that survives macOS PDFKit rendering."""
    configured = os.environ.get("FUTURE_CLINIC_PDF_CJK_FONT")
    if configured:
        candidate = Path(configured).expanduser()
        if not candidate.is_file():
            raise RuntimeError(f"FUTURE_CLINIC_PDF_CJK_FONT does not exist or is not a file: {candidate}")
    else:
        candidate = BUNDLED_PDF_CJK_FONT
        if not candidate.is_file():
            raise RuntimeError(
                f"Bundled PDF CJK font is missing: {candidate}. "
                "Restore the Skill asset or set FUTURE_CLINIC_PDF_CJK_FONT to an explicit compatible .ttf."
            )
    return validate_pdf_cjk_font(candidate)


def pdf_font_face_css(font_path):
    uri = font_path.as_uri()
    faces = []
    for weight in ("400", "700"):
        for style in ("normal", "italic"):
            faces.append(
                "@font-face {\n"
                f'    font-family: "{PDF_CJK_FONT_FAMILY}";\n'
                f'    src: url("{uri}") format("truetype");\n'
                f"    font-weight: {weight};\n"
                f"    font-style: {style};\n"
                "}\n"
            )
    return "\n".join(faces)


# ── CSS 样式 ──
CSS_TEMPLATE = """
FONT_FACE_CSS

@page {
    size: A4;
    margin: 25mm 20mm 20mm 20mm;

    @top-center {
        content: HEADER_TEXT;
        font-family: "Future Clinic PDF CJK", Helvetica, Arial, sans-serif;
        font-size: 8pt;
        color: #95a5a6;
        border-bottom: 0.5pt solid #ecf0f1;
        padding-bottom: 3mm;
    }

    @bottom-center {
        content: "第 " counter(page) " 页";
        font-family: "Future Clinic PDF CJK", Helvetica, Arial, sans-serif;
        font-size: 8pt;
        color: #95a5a6;
        border-top: 0.8pt solid #1a5276;
        padding-top: 2mm;
    }
}

@page :first {
    @top-center { content: none; }
    @bottom-center { content: none; }
}

body {
    font-family: "Future Clinic PDF CJK", Helvetica, Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.75;
    color: #2c3e50;
    text-align: justify;
}

/* 封面 */
.cover {
    page-break-after: always;
    text-align: center;
    padding-top: 45%;
}
.cover h1 {
    font-size: 28pt;
    color: #1a5276;
    margin-bottom: 8mm;
    font-weight: bold;
    letter-spacing: 2pt;
}
.cover .subtitle {
    font-size: 14pt;
    color: #95a5a6;
    margin-bottom: 6mm;
}
.cover .meta {
    font-size: 11pt;
    color: #95a5a6;
    margin-bottom: 4mm;
}
.cover .divider {
    width: 60%;
    margin: 8mm auto;
    border: none;
    border-top: 1.5pt solid #1a5276;
}

/* 一级标题 */
h1 {
    font-size: 20pt;
    color: #1a5276;
    margin-top: 16mm;
    margin-bottom: 6mm;
    padding-bottom: 3mm;
    border-bottom: 2pt solid #1a5276;
    page-break-before: always;
    font-weight: bold;
}

/* 二级标题 */
h2 {
    font-size: 14pt;
    color: #1e8449;
    margin-top: 10mm;
    margin-bottom: 5mm;
    font-weight: bold;
    page-break-after: avoid;
    break-after: avoid;
}

/* 三级标题 */
h3 {
    font-size: 12pt;
    color: #2e86c1;
    margin-top: 6mm;
    margin-bottom: 3mm;
    font-weight: bold;
    page-break-after: avoid;
    break-after: avoid;
}

h4 {
    font-size: 11pt;
    color: #5b2c6f;
    margin-top: 5mm;
    margin-bottom: 2mm;
    font-weight: bold;
    page-break-after: avoid;
    break-after: avoid;
}

/* 段落 */
p {
    margin-top: 1.5mm;
    margin-bottom: 1.5mm;
    orphans: 3;
    widows: 3;
}

/* 引用块 */
blockquote {
    margin: 4mm 0;
    padding: 4mm 4mm 4mm 10mm;
    background: #f8f9fa;
    border-left: 3pt solid #1a5276;
    color: #5d6d7e;
    font-size: 10pt;
}
blockquote p {
    margin: 1mm 0;
}

/* 粗体 */
strong, b {
    font-weight: bold;
    color: #1a252f;
}

/* 行内代码 */
code {
    font-family: "Courier New", "Future Clinic PDF CJK", Courier, monospace;
    background: #fdf2e9;
    color: #c0392b;
    padding: 0.5mm 1.5mm;
    border-radius: 2pt;
    font-size: 9.5pt;
}

/* 表格 */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 4mm 0;
    font-size: 9.5pt;
    table-layout: fixed;
}
thead th {
    background: #1a5276;
    color: white;
    padding: 3mm;
    text-align: left;
    font-weight: bold;
}
th, td { overflow-wrap: anywhere; }
tr { break-inside: avoid; }
thead { display: table-header-group; }
pre { white-space: pre-wrap; overflow-wrap: anywhere; }
img { max-width: 100%; }

tbody td {
    padding: 2.5mm 3mm;
    border-bottom: 0.5pt solid #bdc3c7;
}
tbody tr:nth-child(even) {
    background: #f8f9fa;
}

/* 分隔线 */
hr {
    border: none;
    border-top: 0.5pt solid #bdc3c7;
    margin: 4mm 0;
}

/* 列表 */
ul, ol {
    margin: 2mm 0;
    padding-left: 8mm;
}
li {
    margin-bottom: 1mm;
}

/* 链接 */
a {
    color: #2e86c1;
    text-decoration: none;
}
"""


def md_to_html(md_text, title=None, subtitle="Future Clinic · 未来发展路径会诊",
               meta_line="", author="游诗辰 · Future Clinic", font_face_css=""):
    """Render trusted Markdown; metadata is plain text, not HTML."""
    html_body = markdown.markdown(
        md_text, extensions=["tables", "fenced_code", "nl2br"], output_format="html5"
    )
    first_h1 = re.search(r"<h1>(.*?)</h1>", html_body, flags=re.DOTALL)
    if first_h1:
        extracted_title = html.unescape(re.sub(r"<[^>]+>", "", first_h1.group(1)))
        title = title or extracted_title
        html_body = html_body.replace(first_h1.group(0), "", 1)
    title = title or "Future Clinic"
    # Quote a CSS string independently from HTML text.
    header = json.dumps(f"{title}  |  Future Clinic", ensure_ascii=False)
    header = header.replace("<", r"\3c ")
    css = CSS_TEMPLATE.replace("FONT_FACE_CSS", font_face_css).replace("HEADER_TEXT", header)
    safe_title, safe_author = html.escape(title), html.escape(author)
    safe_subtitle, safe_meta = html.escape(subtitle), html.escape(meta_line)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{safe_title}</title>
    <meta name="author" content="{safe_author}">
    <style>{css}</style>
</head>
<body>
    <div class="cover">
        <h1 style="page-break-before: avoid; border: none;">{safe_title}</h1>
        <div class="subtitle">{safe_subtitle}</div>
        {"<div class='meta'>" + safe_meta + "</div>" if meta_line else ""}
        <hr class="divider">
        <div class="meta">作者: {safe_author}</div>
    </div>
{html_body}
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Future Clinic Markdown → PDF")
    parser.add_argument("input", type=Path, help="Input Markdown file")
    parser.add_argument("output", type=Path, help="New PDF file; existing files are never replaced")
    parser.add_argument("--title", default=None, help="Cover title; defaults to the first Markdown H1")
    parser.add_argument("--author", default="游诗辰 · Future Clinic", help="Author")
    parser.add_argument("--keep-html", action="store_true", help="Also save a new same-stem HTML preview")
    args = parser.parse_args()
    output = args.output.expanduser().absolute()
    preview = output.with_suffix(".html")
    if output.suffix.lower() != ".pdf":
        parser.error("Output must have a .pdf extension")
    for path in ([output, preview] if args.keep_html else [output]):
        if path.exists():
            parser.error(f"Refusing to overwrite existing artifact: {path}")
    source = args.input.expanduser().resolve(strict=True)
    md_text = source.read_text(encoding="utf-8")
    cjk_font = resolve_pdf_cjk_font()
    document = md_to_html(
        md_text, title=args.title, author=args.author,
        font_face_css=pdf_font_face_css(cjk_font),
    )
    from weasyprint import HTML
    pdf = HTML(string=document, base_url=str(source.parent)).write_pdf()
    output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation also protects against a concurrent writer.
    with output.open("xb") as stream:
        stream.write(pdf)
    if args.keep_html:
        with preview.open("x", encoding="utf-8") as stream:
            stream.write(document)
    print(f"[OK] PDF: {output} ({len(pdf) / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
