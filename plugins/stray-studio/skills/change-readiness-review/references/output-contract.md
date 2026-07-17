# Readiness Output Contract

Lead with the decision and make the next action obvious. Use natural Markdown rather than emitting the internal snapshot or a machine-readable schema.

## READY

State that the reviewed state is ready for the named checkpoint. Include:

- the comparison base or PR head identity in a human-readable form;
- the most material verification performed;
- any residual risk that does not control readiness.

Do not list every successful check, fingerprint, file, or suppressed candidate.

## CHANGES_REQUIRED

State the number of blocking findings, then report them by severity. Each finding contains:

- severity and exact location or symbol;
- impact;
- evidence class and concise supporting fact;
- required correction direction.

Do not mix nits or optional redesign into the blocking list. Merge duplicate symptoms with the same cause.

## INCOMPLETE

State:

- which state or evidence could not be fixed or acquired;
- how that gap could change readiness or conceal a blocker; and
- the smallest input, repository state, checkout, permission, or check completion needed for a decisive rerun.

Do not turn an unverified possibility into a finding.

## Display Rules

- Keep internal enum values stable but do not wrap the response in JSON or YAML.
- Keep raw diffs, full snapshots, private PR text, complete OIDs, and fingerprints out of the final response unless a short identifier is necessary to distinguish states.
- Markdown is canonical. Use host-supported inline comments only as a duplicate aid when the workspace exactly matches the reviewed state.
- If remediation was also requested, finish this read-only result and hand confirmed findings to `reviewer` or the relevant implementation skill. Do not edit under this skill.
