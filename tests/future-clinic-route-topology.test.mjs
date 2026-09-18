import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const skill = readFileSync(resolve(here, "../SKILL.md"), "utf8");
const method = readFileSync(
  resolve(here, "../references/future-decision-method.md"),
  "utf8",
);
const contract = `${skill}\n${method}`;

// These are text-contract guards, not a semantic route classifier.
// Non-empty, distinct names cannot establish whether stages or components are alternatives.
// Evaluate that behavior on actual generated narratives and fact-grounded counterexamples.

test("the active contract explores candidates before revisable developmental coordinates", () => {
  assert.doesNotMatch(contract, /固定三路线|恰好三条|exactly three|不得少于或多于三条|继续寻找第三条/);
  assert.match(contract, /较宽候选池|较宽的候选池/);
  assert.match(contract, /所有真实且决策相关的候选必须可见/);
  assert.doesNotMatch(contract, /最小主路线集合/);
  assert.match(contract, /阶段／关键状态骨架/);
  assert.match(contract, /主路线必须完整覆盖/);
});

test("the active contract preserves topology instead of faking parallel alternatives", () => {
  assert.match(contract, /互斥替代/);
  assert.match(contract, /可同时采用/);
  assert.match(contract, /前后阶段/);
  assert.match(contract, /类别与具体实现/);
  assert.match(contract, /条件成立后才激活/);
  assert.match(contract, /共同能力/);
  assert.match(contract, /组合、先后或条件结构/);
});
