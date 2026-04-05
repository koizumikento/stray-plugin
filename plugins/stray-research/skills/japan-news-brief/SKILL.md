---
name: "japan-news-brief"
description: "Use when the user wants a current, source-backed roundup of the latest Japanese news in a fixed briefing format, usually for today, this morning, this evening, or the last 24 hours. Do not use for a deep dive on one event, non-Japan news, or opinion-only coverage."
compatibility: "Requires internet access and a browsing-capable Codex environment because this skill must verify current headlines on the web before answering."
---

# Japan News Brief

Create a concise roundup of the latest Japanese news in a fixed format. Start from live web research every time, anchor all time references in JST, and prefer major Japanese news organizations over blogs, newsletters, or social posts.

When sub-agents are available, prefer using them to split outlet research in parallel and keep the parent agent focused on selection, cross-checking, and final synthesis. If sub-agents are unavailable, fall back to single-agent execution without changing the output format.

Use this skill when the user wants:

- a summary of today's Japanese news
- a morning or evening Japan news briefing
- a fixed-format roundup of recent Japan headlines
- a concise, source-backed domestic news brief for a team or stakeholder

## Do Not Use For

- deep analysis of one specific event or policy debate
- general world news unless it has direct and material impact on Japan
- sports, entertainment, lifestyle, or celebrity coverage unless the user asks for it
- historical explainers that do not require current web verification

## Default Scope

- Focus on Japan domestic politics and administration, economy and business, society and public safety, science and industry, and major international developments that directly affect Japan.
- Default time window to the last 24 hours in JST unless the user specifies another range.
- When the user says "today", "this morning", "latest", or similar relative timing, convert that into an explicit JST date and time range in the output.

## Preferred Source Set

Start with current pages from these official sites and keep the set balanced. Do not rely on one outlet alone when summarizing consequential stories.

- NHK NEWS WEB: [https://www3.nhk.or.jp/news/](https://www3.nhk.or.jp/news/)
- 日本経済新聞: [https://www.nikkei.com/](https://www.nikkei.com/)
- 朝日新聞: [https://www.asahi.com/](https://www.asahi.com/)
- 毎日新聞: [https://mainichi.jp/](https://mainichi.jp/)
- 読売新聞オンライン: [https://www.yomiuri.co.jp/](https://www.yomiuri.co.jp/)
- 47NEWS: [https://www.47news.jp/](https://www.47news.jp/)
- 時事ドットコム: [https://www.jiji.com/](https://www.jiji.com/)
- 産経ニュース: [https://www.sankei.com/](https://www.sankei.com/)

Use the source mix deliberately:

- Prefer NHK for broad public-interest, disaster, government, and breaking domestic coverage.
- Prefer Nikkei when an economic or corporate angle materially changes the significance of a story.
- Use 47NEWS and Jiji to pick up wire-style developments quickly.
- Use national papers to cross-check framing, added detail, and follow-up reporting.

## Workflow

1. Define the brief window before searching.
   - Restate the requested time range in exact JST terms.
   - Note whether the user wants a general brief or a category emphasis.
   - Stop if the user is really asking for a single-topic deep dive rather than a roundup.

2. Choose the execution shape before gathering sources.
   - If sub-agents are available, use them preferentially for bounded source-collection tasks.
   - Give each sub-agent a narrow outlet batch such as NHK plus 47NEWS, Nikkei plus business coverage, and national papers plus wire follow-up.
   - Keep ownership clear: sub-agents collect candidate headlines, links, dates, and short factual notes only.
   - Keep final judgment with the parent agent. The parent decides which stories matter, resolves duplicates, and writes the brief.
   - If sub-agents are unavailable, continue in one agent and gather the same evidence directly.

3. Gather current evidence from the preferred source set.
   - Browse current pages first. Do not answer from memory.
   - Pull from at least 4 current articles across at least 3 distinct outlets unless the news cycle is unusually thin.
   - For major or sensitive claims, confirm with at least 2 independent major outlets when possible.
   - Avoid blogs, AI summaries, link aggregators, commentary columns, and social posts as primary evidence.

4. Select the stories that actually matter.
   - Choose the most consequential Japan-relevant items, not the noisiest items.
   - Prefer developments with clear public, political, economic, safety, or industry impact.
   - Collapse duplicates and near-identical rewrites into one item.
   - If a category has no meaningful update, say so briefly instead of padding the brief.

5. Synthesize without hiding uncertainty.
   - Lead with one short overall summary sentence.
   - For each item, separate confirmed facts from interpretation.
   - Include exact publication or update dates when they matter to recency.
   - Mark paywalled or partially inaccessible sourcing when that affects confidence.

6. Return the brief in the fixed format below.

## Fixed Output Format

Always answer in Japanese unless the user asks otherwise.

```md
# 日本最新ニュースブリーフ
- 対象期間: <YYYY-MM-DD HH:MM JST> から <YYYY-MM-DD HH:MM JST>
- 作成時刻: <YYYY-MM-DD HH:MM JST>
- 総括: <1-2文で全体の流れ>
- 主要参照先: <媒体名リンクをカンマ区切り>

## 1. 政治・行政
- 見出し: <主要トピック>
- 要約: <2-3文>
- 出典: <媒体名リンク> (<公開日または更新日>)

## 2. 経済・ビジネス
- 見出し: <主要トピック or 大きな更新なし>
- 要約: <2-3文 or 1文>
- 出典: <媒体名リンク> (<公開日または更新日>)

## 3. 社会・災害・安全
- 見出し: <主要トピック or 大きな更新なし>
- 要約: <2-3文 or 1文>
- 出典: <媒体名リンク> (<公開日または更新日>)

## 4. 産業・テクノロジー
- 見出し: <主要トピック or 大きな更新なし>
- 要約: <2-3文 or 1文>
- 出典: <媒体名リンク> (<公開日または更新日>)

## 5. 国際動向と日本への影響
- 見出し: <主要トピック or 大きな更新なし>
- 要約: <2-3文 or 1文>
- 出典: <媒体名リンク> (<公開日または更新日>)

## 6. 続報待ちメモ
- <未確定情報、続報待ちの論点、または「特になし」>
```

## Output Expectations

- Keep the brief compact enough to scan quickly.
- Include live links for every story slot that contains a real item.
- Use exact JST dates instead of ambiguous relative timing.
- Keep one item per section unless the user explicitly asks for a longer digest.
- Say "大きな更新なし" or "特になし" when needed instead of inventing weak filler.

## Guardrails

- Do not skip web research. This skill is current by definition.
- Prefer sub-agents when available, but do not fail just because they are unavailable.
- Do not rely on one outlet for the whole brief.
- Do not let sub-agents write the final brief independently; the parent agent must integrate and normalize the output.
- Do not present editorial framing as confirmed fact.
- Do not turn the roundup into a long essay.
- Do not hide uncertainty when stories are still moving.
- Do not drift into sports or entertainment unless the user asks for them.
