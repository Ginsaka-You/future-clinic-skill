# 独立 PDF 渲染

所有渲染代码、样式与中文字体均在本 Skill 内；不需要安装其他 Skill。仍需 Python 和下列开源运行库。

## 环境

先检查宿主提供的 Python 或 `FUTURE_CLINIC_PDF_PYTHON` 指向的解释器能否导入 `markdown`、`weasyprint`、`fontTools`。缺少依赖时，依当前授权在本仓库建立隔离环境，不改系统 Python：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Python 需要 3.10 或更高版本。WeasyPrint 还需要系统字体与排版库；如果导入失败，按 [WeasyPrint 安装说明](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation) 检查对应平台的 Pango 等依赖和动态库发现。已有运行库不要重复安装。不要使用 `--break-system-packages`，也不要通过重启桌面应用解决依赖问题。

## 调用

从 Skill 根目录运行（在其他目录运行时改用该脚本的实际绝对路径）：

```sh
.venv/bin/python scripts/md_to_pdf.py \
  examples/阶段与路径示例.md output/阶段与路径示例.pdf \
  --author "游诗辰 · Future Clinic"
```

默认以 Markdown 第一个一级标题作为封面标题，`--title` 可以显式指定同一标题。默认不保存 HTML；需要排查版式时加 `--keep-html`。输出文件已存在时拒绝覆盖，请按报告命名规则换用新的同主名 Markdown/PDF 文件。

字体默认读取仓库内 `assets/NotoSansSC[wght].ttf`。如需替换，可设置 `FUTURE_CLINIC_PDF_CJK_FONT` 为有简体中文字形的 TrueType `.ttf` 文件；脚本会检查格式和代表性中文字形，不代表它覆盖任意语言或符号。字体来源和许可见 `assets/NotoSansSC-SOURCE.txt` 与 `assets/OFL-NotoSansSC.txt`。

只渲染已审阅的 Markdown。它可包含原始 HTML、图片和相对文件路径；渲染器不是不可信文档的安全沙箱，可能加载文档引用的本地或网络资源。不要把它作为无隔离的公开文件转换服务。

## 验证

```sh
node --test tests/*.test.mjs
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
```

文字合同测试不证明研究质量。每份最终 PDF 仍应检查文本、链接、标题和作者，并逐页检查中文、裁切、表格与分页；具体研究交付要求见 `future-decision-method.md` 第 7 节。示例只用于排版和渲染检查，不是实际会诊报告。
