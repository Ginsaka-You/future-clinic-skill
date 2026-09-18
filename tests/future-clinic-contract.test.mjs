import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
const skill = readFileSync(resolve(here, "../SKILL.md"), "utf8");
const method = readFileSync(
  resolve(here, "../references/future-decision-method.md"),
  "utf8",
);
const openai = readFileSync(resolve(here, "../agents/openai.yaml"), "utf8");
const contract = `${skill}\n${method}`;

test("explicit invocation remains the only gate and starts unconditionally", () => {
  assert.match(skill, /只在用户显式调用[^\n]+时运行/);
  assert.match(skill, /一旦调用就无条件启动 Future Clinic/);
  assert.match(skill, /不得在候选生成前运行任何决定是否进入/);
});

test("the shared diagnostic base is naturally elastic and crosses four evidence dimensions", () => {
  assert.match(contract, /共享深度诊断底座/);
  assert.match(contract, /当前事实[^\n]+未知[^\n]+边界/);
  assert.match(contract, /纵向[^\n]+形成[^\n]+演化/);
  assert.match(contract, /横向[^\n]+竞争解释/);
  assert.match(contract, /交叉[^\n]+矛盾[^\n]+驱动力/);
  assert.match(contract, /自然伸缩/);
});

// Static contract guards only; generated decisions need independent behavioral review.
test("pathway instructions retain shared capabilities and substantive depth", () => {
  assert.ok(!contract.includes("候选至少改变当前第一选择"), "obsolete sufficient-difference rule must not coexist with pathway semantics");
  assert.match(contract, /共同能力/);
  assert.match(contract, /子分支/);
  assert.match(contract, /条件路线/);
  assert.match(contract, /主路线必须完整覆盖/);
  assert.match(contract, /参与者反应/);
  assert.match(contract, /稳定[／/]失败形态/);
  assert.match(contract, /不可逆成本/);
  assert.match(contract, /选择权/);
  assert.match(contract, /换路信号/);
});

test("two hops are a minimum checkpoint, not a hard stop", () => {
  assert.match(contract, /两跳[^\n]+最低检查点/);
  assert.match(contract, /稳定[^\n]+失败[^\n]+下一次决策/);
  assert.doesNotMatch(contract, /默认两跳/);
  assert.doesNotMatch(contract, /回到两跳/);
});

test("the native chip carries the developmental coordinates and explicit invocation contract", () => {
  assert.match(openai, /shared deep diagnostic base/);
  assert.match(openai, /decision-relevant candidates/);
  assert.match(openai, /stages or key states/);
  assert.match(openai, /allow_implicit_invocation: false/);
});
