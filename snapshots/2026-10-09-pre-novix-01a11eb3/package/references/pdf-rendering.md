# 独立 PDF 渲染

渲染脚本、样式和中文字体都随本 Skill 提供，不依赖其他 Skill。仅渲染已审阅的 Markdown；原始 HTML、图片及链接可加载本地或网络资源，这不是不可信文档的安全沙箱。

先检查宿主提供的 Python 或 `FUTURE_CLINIC_PDF_PYTHON` 是否可导入 `markdown`、`weasyprint`、`fontTools`。已有依赖先修复路径或动态库发现；确实缺失才按宿主授权用兼容 Python（3.10+）和本 Skill 的 `requirements.txt` 建立隔离环境。Pango 等排版库问题参照 [WeasyPrint 安装说明](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation)，不改系统安全设置，不用 `--break-system-packages`，不重启桌面应用。

调用已确认的 Python，并把示例路径换成实际文件：

```sh
python /实际路径/future-clinic/scripts/md_to_pdf.py /实际路径/主题.md /实际路径/主题.pdf --author "游诗辰 · Future Clinic"
```

默认以第一个一级标题作封面标题。需要排版诊断时加 `--keep-html`。已有输出拒绝覆盖；用新的同主名 Markdown/PDF 保留历史。

默认字体为 `assets/NotoSansSC[wght].ttf`，来源和许可分别为 `assets/NotoSansSC-SOURCE.txt`、`assets/OFL-NotoSansSC.txt`。必要时用 `FUTURE_CLINIC_PDF_CJK_FONT` 指向有中文字形的 TrueType 字体；程序检查代表性字形，不保证任意符号或语言都覆盖。

生成后核对标题、作者、正文、表格和来源链接，并逐页查看；检查原则见 [future-decision-method.md](future-decision-method.md) 第8节。文本或结构测试不证明报告有主线，也不替代视觉检查。
