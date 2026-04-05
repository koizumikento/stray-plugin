# Code Review Best Practices

This note captures the external guidance used to shape `code-reviewer`.

## Working Defaults

- Focus on substantive defects first: correctness, security, performance, reliability, and test gaps.
- Keep feedback specific, actionable, and tied to exact code locations.
- Treat review as a lightweight quality gate, not a demand for a perfect redesign.
- Use automation for mechanical issues so human review time stays on higher-value concerns.
- Treat AI review as a supplement to human review, especially for large or high-risk changes.
- Be explicit about uncertainty, missed-context risk, and false-positive risk.

## Source Notes

### GitHub Docs: "Code reviewer"

GitHub's customization example for code review emphasizes structured attention to security, performance, and code quality, along with review style guidance to be specific, actionable, explanatory, and clarifying when intent is unclear.

Link: https://docs.github.com/en/copilot/tutorials/customization-library/custom-instructions/code-reviewer

### GitHub Docs: "Responsible use of GitHub Copilot code review"

GitHub recommends using AI review to supplement human reviews rather than replace them. The doc also highlights three operational limits that shaped this skill:

- missed issues, especially in large or complex changes
- false positives caused by misunderstandings or hallucinations
- generated suggestions that may still be incorrect or insecure

The doc also notes that better contextual inputs, such as change descriptions and custom instructions, improve review quality.

Link: https://docs.github.com/en/copilot/responsible-use/code-review

### Software Engineering at Google, Chapter 9

Google's code review guidance influenced the reviewer posture in this skill:

- review should check correctness, comprehensibility, consistency, and testing
- lightweight processes scale better than heavyweight ones
- reviewers should approve changes that improve the codebase instead of blocking on a more perfect solution
- automation should absorb mechanical checks so reviewers can focus on higher-order concerns

Link: https://abseil.io/resources/swe-book/html/ch09.html

## Implications For This Skill

- Findings-first output is intentional because reviewers should surface the highest-risk issue first.
- Confirmed evidence is required before reporting a defect because AI review can hallucinate.
- "No findings" still requires residual-risk commentary so the user understands what was and was not verified.
- The workflow explicitly asks for context and nearby code because review quality drops when the diff is read in isolation.

## Related Aspect Packs

Use these focused references instead of bloating `SKILL.md` with stack-specific detail:

- `review-aspects-core.md` for almost every review
- `backend-security-and-reliability.md` for APIs, services, jobs, and infra-adjacent changes
- `frontend-and-accessibility.md` for UI and client-side changes
- `data-and-migrations.md` for schema, migration, and persistent-data changes
