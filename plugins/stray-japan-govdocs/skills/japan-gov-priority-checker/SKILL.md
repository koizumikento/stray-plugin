---
name: "japan-gov-priority-checker"
description: "Use when the user asks whether a theme is a current or rising Japanese government priority, whether official emphasis has strengthened, or whether a topic is policy-relevant. Do not use for pure evidence gathering, one-document summaries, or legal/procedural questions."
---

# Japan Gov Priority Checker

Check whether a theme is treated as a priority in Japanese government whitepapers and official policy documents.

Use this skill when the user asks:

- "防災DXは国として本当に重視されてる?"
- "買い物弱者対策は政策上強まっている?"
- "このテーマは今提案する文脈がある?"

## Workflow

1. Define the theme and what "priority" means for the user's use case.
2. Check latest whitepapers and relevant ministry policy pages.
3. Compare with the previous edition when emphasis change matters.
4. Look for signals: dedicated sections, repeated terms, new measures, budget or program mentions, KPI language, council plans, or cross-ministry recurrence.
5. Separate confirmed priority signals from inference.

## Output Expectations

- `結論`: high / medium / low / unclear
- `優先度シグナル`
- `過年度からの変化`
- `関連省庁・資料`
- `提案・調査での使い方`
- `注意点`

## Guardrails

- Do not infer priority from word count alone.
- Do not predict future budget or adoption.
- Do not ignore publication date and edition lag.
