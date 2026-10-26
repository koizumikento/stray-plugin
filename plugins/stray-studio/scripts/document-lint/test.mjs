import assert from "node:assert/strict";
import { copyFileSync, mkdtempSync, readFileSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import test from "node:test";

const root = fileURLToPath(new URL(".", import.meta.url));
const checker = join(root, "check.mjs");

function fixture(t, text, extension = ".md") {
  const cwd = mkdtempSync(join(tmpdir(), "document-lint-"));
  t.after(() => rmSync(cwd, { recursive: true, force: true }));
  const path = join(cwd, `原稿 with spaces${extension}`);
  writeFileSync(path, text);
  return { cwd, path };
}

function run(cwd, args, script = checker) {
  const result = spawnSync(process.execPath, [script, ...args], { cwd, encoding: "utf8" });
  assert.ifError(result.error);
  return result;
}

test("common profile warns about selected product spellings, including emphasis", (t) => {
  const { cwd, path } = fixture(t, "Github と **Chatgpt** と NodeJS を使う。\n");
  const result = run(cwd, [path]);
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /errors=0 warnings=3/);
  assert.match(result.stdout, /warning prh/);
});

test("preserves uncertainty, correct terms, code, URLs, and quotations without writing", (t) => {
  const text = "# 調査\n\nGitHub と ChatGPT と Node.js を使う可能性がある。\n\n" +
    "`Github`\n\n```text\nChatgpt\n#見出し\n```\n\n" +
    "> Github という原文の引用。\n\n[原文](https://example.com/Github)\n";
  const { cwd, path } = fixture(t, text);
  const result = run(cwd, ["--ja", "--", path]);
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /errors=0 warnings=0/);
  assert.equal(readFileSync(path, "utf8"), text);
});

test("Markdown errors fail, but text files are not parsed as Markdown", (t) => {
  const text = "#見出し\n\n(説明)[https://example.com]\n";
  const markdown = fixture(t, text);
  const result = run(markdown.cwd, [markdown.path]);
  assert.equal(result.status, 1, result.stderr);
  assert.match(result.stdout, /error MD011/);
  assert.match(result.stdout, /error MD018/);
  const plain = fixture(t, text, ".txt");
  assert.equal(run(plain.cwd, [plain.path]).status, 0);
});

test("Japanese length warns above 100 code units, is opt-in, and never hides Markdown errors", (t) => {
  const { cwd, path } = fixture(t, "あ".repeat(99) + "。\n");
  const boundary = run(cwd, ["--ja", path]);
  assert.equal(boundary.status, 0, boundary.stderr);
  assert.match(boundary.stdout, /errors=0 warnings=0/);
  writeFileSync(path, "あ".repeat(100) + "。\n");
  const warning = run(cwd, ["--ja", path]);
  assert.equal(warning.status, 0, warning.stderr);
  assert.match(warning.stdout, /warning sentence-length/);
  assert.match(warning.stdout, /errors=0 warnings=1/);
  assert.match(run(cwd, [path]).stdout, /errors=0 warnings=0/);
  writeFileSync(path, "#見出し\n\nGithub は" + "あ".repeat(100) + "。\n");
  const mixed = run(cwd, ["--ja", path]);
  assert.equal(mixed.status, 1, mixed.stderr);
  assert.match(mixed.stdout, /error MD018/);
  assert.match(mixed.stdout, /warning prh/);
  assert.match(mixed.stdout, /warning sentence-length/);
  assert.match(mixed.stdout, /errors=1 warnings=2/);
});

test("narrow suppression protects deliberate bad examples", (t) => {
  const text = "<!-- textlint-disable prh -->\nGithub\n<!-- textlint-enable prh -->\n\n" +
    "<!-- markdownlint-disable-next-line MD018 -->\n#見出し\n";
  const { cwd, path } = fixture(t, text);
  const suppressed = run(cwd, [path]);
  assert.equal(suppressed.status, 0, suppressed.stderr);
  assert.match(suppressed.stdout, /errors=0 warnings=0/);
  writeFileSync(path, text + "\nGithub\n");
  const following = run(cwd, [path]);
  assert.equal(following.status, 0, following.stderr);
  assert.match(following.stdout, /errors=0 warnings=1/);
});

test("inline quotations and plain-text identifiers remain advisory and unchanged", (t) => {
  for (const [text, extension] of [
    ["「Github」と原文に書かれていました。\n", ".md"],
    ["NodeJS という識別子です。\n", ".txt"],
  ]) {
    const { cwd, path } = fixture(t, text, extension);
    const result = run(cwd, [path]);
    assert.equal(result.status, 0, result.stderr);
    assert.match(result.stdout, /warning prh/);
    assert.match(result.stdout, /errors=0 warnings=1/);
    assert.equal(readFileSync(path, "utf8"), text);
  }
});

test("known hashtag and regex false positives allow only a narrow Markdown exception", (t) => {
  for (const [rule, text] of [
    ["MD018", "#hashtag\n"],
    ["MD011", "(^|/)[Cc]+odespace/\n"],
  ]) {
    const { cwd, path } = fixture(t, text);
    const original = run(cwd, [path]);
    assert.equal(original.status, 1, original.stderr);
    assert.match(original.stdout, new RegExp(`error ${rule}`));
    assert.equal(readFileSync(path, "utf8"), text);
    const exception = `<!-- Intentional literal. -->\n<!-- markdownlint-disable-next-line ${rule} -->\n${text}`;
    writeFileSync(path, exception);
    const allowed = run(cwd, [path]);
    assert.equal(allowed.status, 0, allowed.stderr);
    assert.match(allowed.stdout, /errors=0 warnings=0/);
    writeFileSync(path, exception + "\n" + text);
    const following = run(cwd, [path]);
    assert.equal(following.status, 1, following.stderr);
    assert.match(following.stdout, /errors=1 warnings=0/);
  }
});

test("invalid, missing, empty, or directory targets fail instead of passing with zero files", (t) => {
  const { cwd } = fixture(t, "");
  for (const args of [[], ["--fix"], [join(cwd, "missing.md")], [cwd]]) {
    const result = run(cwd, args);
    assert.equal(result.status, 2, JSON.stringify(args));
    assert.match(result.stderr, /document-lint unavailable/);
  }
});

test("caller configuration and ignore files cannot skip explicit targets", (t) => {
  const { cwd, path } = fixture(t, "#見出し\n\nGithub\n");
  writeFileSync(join(cwd, ".textlintignore"), "**/*\n");
  writeFileSync(join(cwd, ".textlintrc.json"), '{"rules": {}}');
  writeFileSync(join(cwd, ".markdownlint.json"), '{"default": false}');
  const result = run(cwd, [path]);
  assert.equal(result.status, 1, result.stderr);
  assert.match(result.stdout, /error MD018/);
  assert.match(result.stdout, /errors=1 warnings=1/);
});

test("missing dependencies or bundled configuration fail closed", (t) => {
  const { cwd, path } = fixture(t, "GitHub\n");
  for (const name of ["check.mjs", "markdownlint.json", "terms.yml"]) {
    copyFileSync(join(root, name), join(cwd, name));
  }
  const isolatedChecker = join(cwd, "check.mjs");
  const missingDependencies = run(cwd, [path], isolatedChecker);
  assert.equal(missingDependencies.status, 2);
  assert.match(missingDependencies.stderr, /document-lint unavailable/);
  symlinkSync(join(root, "node_modules"), join(cwd, "node_modules"), "dir");
  assert.equal(run(cwd, [path], isolatedChecker).status, 2);
  writeFileSync(join(cwd, "textlint.json"), "{broken");
  assert.equal(run(cwd, [path], isolatedChecker).status, 2);
  copyFileSync(join(root, "textlint.json"), join(cwd, "textlint.json"));
  assert.equal(run(cwd, ["--ja", path], isolatedChecker).status, 2);
});
