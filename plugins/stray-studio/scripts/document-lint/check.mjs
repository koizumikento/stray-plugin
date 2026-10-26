import { readFile } from "node:fs/promises";
import { extname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

async function main() {
  const args = process.argv.slice(2);
  const japanese = args[0] === "--ja";
  if (japanese) args.shift();
  if (args[0] === "--") args.shift();
  if (!args.length) {
    throw new Error("Usage: node check.mjs [--ja] [--] FILE.md|FILE.txt ... (explicit files only)");
  }
  const paths = [...new Set(args.map((path) => resolve(path)))];
  for (const path of paths) {
    if (![".md", ".txt"].includes(extname(path))) {
      throw new Error(`Expected a .md or .txt file: ${path}`);
    }
  }
  const { createLinter, loadTextlintrc } = await import("textlint");
  const { lint } = await import("markdownlint/sync");
  const load = (name) => loadTextlintrc({
    configFilePath: fileURLToPath(new URL(name, import.meta.url)),
    node_modulesDir: fileURLToPath(new URL("node_modules/", import.meta.url)),
  });
  let descriptor = await load("textlint.json");
  if (japanese) descriptor = descriptor.concat(await load("textlint-ja.json"));
  // textlint returns an empty descriptor when configuration loading fails.
  if (descriptor.toKernelOptions().rules.length !== (japanese ? 2 : 1)) {
    throw new Error("Bundled textlint rules did not load; check configuration and npm ci.");
  }
  const linter = createLinter({ descriptor });
  const markdownConfig = JSON.parse(await readFile(new URL("markdownlint.json", import.meta.url), "utf8"));
  let errors = 0;
  let warnings = 0;
  for (const path of paths) {
    const text = await readFile(path, "utf8");
    // lintText avoids silently skipping explicit targets through the caller's ignore files.
    const result = await linter.lintText(text, path);
    for (const message of result.messages) {
      const warning = message.severity === 1;
      if (warning) warnings++; else errors++;
      console.log(`${path}:${message.line} ${warning ? "warning" : "error"} ${message.ruleId} ${message.message}`);
    }
    if (extname(path) === ".md") {
      const results = lint({ strings: { [path]: text }, config: markdownConfig });
      for (const message of results[path]) {
        errors++;
        console.log(`${path}:${message.lineNumber} error ${message.ruleNames[0]} ${message.ruleDescription}`);
      }
    }
  }
  console.log(`document-lint files=${paths.length} errors=${errors} warnings=${warnings} profile=${japanese ? "ja" : "common"}`);
  process.exitCode = errors ? 1 : 0;
}

main().catch((error) => {
  console.error(`document-lint unavailable: ${error.message}`);
  process.exitCode = 2;
});
