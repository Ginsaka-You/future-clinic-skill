import assert from 'node:assert/strict';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { dirname, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = path => readFileSync(resolve(root, path), 'utf8');
const skill = read('SKILL.md');
const ui = read('agents/openai.yaml');

// Package integrity only. These checks cannot judge relationships, reasoning or readability.
// Use actual full-report forward runs and source-bound reading for behavioral evidence.
test('the package identifies the explicit-only Future Clinic entry', () => {
  const frontmatter = skill.match(/^---\n([\s\S]+?)\n---/);
  assert.ok(frontmatter, 'YAML frontmatter exists');
  assert.match(frontmatter[1], /^name: future-clinic$/m);
  assert.match(frontmatter[1], /^description: "[^\n]+"$/m);
  assert.match(ui, /^  allow_implicit_invocation: false$/m);
  assert.match(ui, /^  default_prompt: "Use \$future-clinic /m);
  assert.match(ui, /^  display_name: "Future Clinic"$/m);
});

test('all relative instruction references resolve inside the package', () => {
  const files = ['SKILL.md', ...readdirSync(resolve(root, 'references')).filter(n => n.endsWith('.md')).map(n => `references/${n}`)];
  for (const file of files) {
    for (const match of read(file).matchAll(/\[[^\]]*\]\(([^)]+)\)/g)) {
      const target = match[1];
      if (/^https?:/.test(target) || target.startsWith('#')) continue;
      const absolute = resolve(root, dirname(file), target.split('#')[0]);
      assert.ok(absolute.startsWith(root + sep), `${file}: outside-package reference`);
      assert.ok(existsSync(absolute), `${file}: missing ${target}`);
    }
  }
});

test('standalone rendering resources and license are present', () => {
  for (const file of ['scripts/md_to_pdf.py', 'requirements.txt', 'assets/NotoSansSC[wght].ttf', 'assets/OFL-NotoSansSC.txt', 'assets/NotoSansSC-SOURCE.txt']) {
    assert.ok(existsSync(resolve(root, file)), `missing ${file}`);
  }
});

test('active instructions and renderer contain no external skill path or local user path', () => {
  for (const file of ['SKILL.md', 'agents/openai.yaml', 'references/future-decision-method.md', 'references/pdf-rendering.md', 'scripts/md_to_pdf.py']) {
    assert.doesNotMatch(read(file), /(?:\.codex|\.agents)\/skills\/[^/]+\/scripts|\/Users\//);
  }
});
