import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

const read = (relative) => readFileSync(new URL(relative, import.meta.url), "utf8");
const skill = read("../SKILL.md");
const method = read("../references/future-decision-method.md");
const ui = read("../agents/openai.yaml");

// Narrow instruction-regression guards only. They do not grade generated reports.
// Real generation and source-bound reading results live outside the installed Skill.
test("diagram delivery is optional in all active instructions", () => {
  for (const text of [skill, method]) {
    assert.match(text, /图是可选辅助/);
    assert.doesNotMatch(text, /总体因果路线图必交|每次会诊必须交付可独立理解的\*\*总体因果路线图|无图形工具就交清楚的文本关系图/);
  }
  assert.match(ui, /diagrams are optional/);
});

test("the output contract requires direct nesting and stage-by-stage review", () => {
  assert.match(skill, /每个有实质选择的阶段下面/);
  assert.match(method, /无需翻其他章节或图就知道父子关系/);
  assert.match(skill, /不能只抽查最好懂的一条/);
  assert.match(method, /阶段内路径/);
  assert.match(method, /成品短例/);
});
