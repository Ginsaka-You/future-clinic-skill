import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const skill = readFileSync(resolve(here, "../SKILL.md"), "utf8");
const method = readFileSync(
  resolve(here, "../references/future-decision-method.md"),
  "utf8",
);
const contract = `${skill}\n${method}`;

test("a current Future Brief is reused but never treated as evidence", () => {
  assert.match(contract, /Future Brief/);
  assert.match(contract, /目标与输入索引/);
  assert.match(contract, /不是外部事实的证明/);
  assert.match(contract, /不(?:要)?重复询问[^\n]*已经解决/);
  assert.match(contract, /仍然有效/);
});

test("absence of a Brief does not gate entry", () => {
  assert.match(skill, /一旦调用就无条件启动 Future Clinic/);
  assert.match(contract, /没有 Future Brief[^\n]*(?:仍然|仍)[^\n]*(?:启动|无条件启动)/);
  assert.match(contract, /快速就绪检查/);
  assert.match(contract, /能查[^\n]*先查/);
});

test("late critical user-only unknowns stop the final report exactly at the safety boundary", () => {
  assert.match(contract, /深度研究[^\n]*新发现[^\n]*关键用户未知/);
  assert.match(contract, /只有用户知道/);
  assert.match(contract, /安全性/);
  assert.match(contract, /当前问题模型/);
  assert.match(contract, /第一步行动/);
  assert.match(contract, /主路线/);
  assert.match(contract, /停止[^\n]*不生成最终报告/);
  assert.match(contract, /自然语言停问|自然提问/);
  assert.match(contract, /同一已启动会诊内继续/);
  assert.match(contract, /无须重新调用 Skill/);
  assert.doesNotMatch(contract, /用户回答后(?:需)?再次手动调用/);
  assert.match(contract, /非关键未知[^\n]*(?:假设|条件分支|范围收窄|换路信号)/);
});

test("semantic Markdown and PDF names share one non-overwriting stem", () => {
  assert.match(contract, /report_title/);
  assert.match(contract, /artifact_stem/);
  assert.match(contract, /用户明确指定报告名称时优先使用/);
  assert.match(contract, /Markdown 与 PDF 使用完全相同的实际主名/);
  assert.match(contract, /[\\/:*?"<>|]/);
  assert.match(contract, /_2[^\n]*_3/);
  assert.match(contract, /不得覆盖旧产物/);
  assert.match(contract, /聊天链接[^\n]*实际名称/);
  assert.doesNotMatch(contract, /唯一 report\.md|派生 report\.pdf|`report\.md`|`report\.pdf`/);
});

test("report byline is explicit in the Skill and PDF rendering contract", () => {
  assert.ok(
    skill.includes("报告署名统一为 `游诗辰 · Future Clinic`"),
    "The Skill must specify the requested report author",
  );
  assert.ok(
    method.includes('--author "游诗辰 · Future Clinic"'),
    "PDF rendering must explicitly pass the requested author",
  );
  assert.ok(
    method.includes("提取文本核对标题、署名"),
    "PDF verification must include the visible byline",
  );
});
