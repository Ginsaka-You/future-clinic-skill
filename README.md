# Future Clinic

把未来研究组织成可读的发展过程：**阶段 → 该阶段的问题 → 具体路径 → 反馈与后续**。

Future Clinic 是可独立安装的 Agent Skill。它根据事实、形成机制、竞争解释与关键未知展开候选，在每个阶段下比较真实选择，再说明反馈怎样影响下一步。它不固定阶段数或路径数；图是可选辅助，文字本身必须讲清整体框架。

## 使用

下载本仓库，或克隆为名为 `future-clinic` 的文件夹：

```sh
git clone https://github.com/Ginsaka-You/future-clinic-skill.git future-clinic
```

将这个文件夹放到所用宿主支持的 Skill 目录，按宿主方式加载。入口为根目录的 `SKILL.md`；`agents/openai.yaml` 包含 Codex 的显示信息与显式调用设置。这里提供的是 Skill 仓库，不是已经上架的 ChatGPT 插件，跨宿主的发现、调用和工具权限需分别验证。

在支持相应语法的宿主中显式调用：

```text
$future-clinic 研究怎样组织一个小型读书活动：先说明发展阶段，
再比较每个阶段的做法，以及反馈出现后怎样继续或换路。
```

可以先用 [Future Brief](https://github.com/Ginsaka-You/future-brief-skill) 整理目标与事实，但它不是运行 Clinic 的前提，也不会自动调用 Clinic。

## 交付与运行条件

- 一份完整 Markdown、一份同源同主名 PDF、聊天摘要。
- 研究需要宿主提供适当的文件与联网能力；本仓库不提供模型或搜索服务。
- PDF 渲染脚本、样式和中文字体内置，不依赖其他 Skill。
- PDF 运行环境与命令见 [渲染说明](references/pdf-rendering.md)，依赖版本见 `requirements.txt`。
- 默认署名为 `游诗辰 · Future Clinic`。示例和代码不包含个人业务报告或会话记录。

## 边界

会诊默认研究与设计，不授权采购、发送消息、部署或改动业务系统。预测保留条件与未知，不保证未来结果；不能把静态测试通过当成研究质量或现实效果证明。

维护者可运行 `node --test tests/*.test.mjs` 与渲染说明中的 Python 测试。`examples/阶段与路径示例.md` 是虚构的渲染样例。

## 许可

中文字体按随附 SIL Open Font License 1.1 分发，版权及来源保留在 `assets/`。本仓库其余内容尚未另附开源许可证。
