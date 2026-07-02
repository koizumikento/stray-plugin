# Source Guide

Use this guide when collecting, evaluating, or citing Japanese horse racing data.

## Source Priority

1. Official or licensed data available to the user
   - JRA official race pages
   - JRA-VAN Data Lab. / JV-Data when the user has access
   - NAR / keiba.go.jp official pages and downloadable CSV files
2. User-provided data
   - CSV, PDF, screenshots, race cards, odds captures, notes, or private datasets the user is allowed to use
3. Secondary public pages
   - Use only when terms permit the intended use, and avoid automated collection when terms are unclear or restrictive

## Practical Source Notes

- JRA official pages are suitable for current race context such as entries, odds, results, horse search, jockey/trainer data, and related official notices.
- JRA-VAN Data Lab. is a licensed data service accessed through JV-Link/JV-Data. Treat it as user-provided or user-authorized data, not as a public web API.
- NAR official downloads can provide CSV data for race cards, payouts, race lists, and odds. Record file date and update timing.
- netkeiba and similar databases can be useful for manual reference, but do not make automated scraping or redistribution the default workflow. Check terms first.
- User screenshots and copied tables are acceptable inputs when the user provides them; preserve source name and capture time.

## Permission Check

Before collecting data automatically, check:

- Is the source official, licensed, or explicitly user-provided?
- Does the site allow automated access, reproduction, redistribution, or commercial use for this workflow?
- Is login, paid access, or an API key required?
- Are robots, rate limits, or terms unclear?
- Will the output reproduce a substantial source database or only summarize a specific race analysis?

If permission is unclear or restrictive, do not automate collection. Ask for user-provided files or use an official source that can be accessed safely.

Treat permission as unclear in cases like these:

- robots or crawling rules do not mention the path, and the site's terms of use cannot be located
- the terms allow only 私的利用 or personal viewing and say nothing about analysis or excerpting
- the data appears on an aggregator that republishes official data without a visible license
- access requires login or paid membership and the terms for programmatic use are not stated

## Freshness Rules

Always record the timestamp or date for:

- Odds
- Scratches, cancellations, and jockey changes
- Body weight and body-weight change
- Weather and going
- Race card and post position
- Final odds or payout data used for review

Warn the user when analysis is based on early odds or stale race data. Late odds movement can materially change value conclusions.

## Citation Rules

- Name every source used in the answer.
- Link web sources when browsing is used.
- For user-provided files, name the file or describe the artifact.
- Separate facts copied from a source from inference made during analysis.
- Do not overquote; summarize race data and cite the source.

## Stop Conditions

- Stop automated collection if source terms prohibit or likely prohibit the intended access.
- Stop ticket suggestions if current odds, scratches, or body weight are unavailable for a race near post time.
- Stop any request to operate betting accounts, place wagers, bypass access controls, or purchase on behalf of the user.
