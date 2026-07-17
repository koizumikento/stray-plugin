# Pull Request Review-Request Gate

Use this adapter only when the pull-request author asks whether an open PR is ready for an initial or repeat human review request.

## Establish The Target

1. Fix `owner/repository`, PR number, and the current open PR.
2. Use cycle `initial` before the first human review request.
3. Use cycle `rerequest` after fixes when the author is deciding whether to request another review.
4. If authorship or cycle changes the requested decision and cannot be established safely, return `INCOMPLETE` or ask for the missing identity.

## Capture

Use an authenticated `gh` CLI, create an external temporary directory, and capture the initial state:

```bash
snapshot_dir=$(mktemp -d)
chmod 700 "$snapshot_dir"
python3 scripts/capture_pr_state.py \
  --repo <owner/repository> \
  --pr <number> \
  --cycle <initial|rerequest> \
  --workspace-root <current-workspace> \
  --snapshot-dir "$snapshot_dir" \
  --name initial \
  --write-diff
```

The helper uses GitHub read endpoints, validates paginated list counts where GitHub exposes totals, captures linked closing Issues, binds checks to the exact head OID, fingerprints the raw diff, and writes snapshots and the optional diff with exclusive mode-600 creation outside the declared workspace. Standard output contains only a summary.

## Initial And Repeat Review

- `initial` loads PR metadata, commits, files, head checks/statuses, and the raw diff. It does not fetch historical discussion merely because it exists.
- `rerequest` additionally loads reviews, issue comments, review comments, and review-thread resolution state.
- Gate only explicit change requests and feedback that independently satisfies the current blocking policy. Do not gate on acknowledgements, status messages, optional suggestions, nits, or unanswered questions without a confirmed failure path.
- A resolved historical finding is not a new finding. Report unresolved blockers and summarize resolved feedback without expanding a ledger the author cannot act on.

## Completeness And Checks

- The final commit returned by GitHub must equal the PR head OID.
- Every check run used in the decision must target that same head OID. Never reuse success from an older commit.
- A missing or pending check is a proof gap. It becomes `INCOMPLETE` only when that check can materially conceal a blocking defect or is a required repository gate.
- If GitHub returns incomplete pagination, inconsistent counts, missing textual patches that require inspection, or a diff at conservative host limits, do not declare readiness from the remote diff. Use an exact clean checkout of the base/head OIDs when safely available; otherwise return `INCOMPLETE`.
- Local unpushed changes are outside the PR and cannot support PR readiness.

## Freshness Check

Immediately before deciding, rerun the same command with `--name final` and without `--write-diff`. Compare the complete snapshot fingerprints.

- A changed head OID, base OID, diff, file list, checks, or relevant rerequest feedback invalidates the initial decision.
- Re-review only when the new state can be acquired and checked completely; otherwise return `INCOMPLETE`.
- Delete all snapshots, raw diffs, and the temporary directory after the result is fixed.

## Read-Only Boundary

Do not checkout, reset, fetch solely for inline display, submit a review, resolve a thread, request reviewers, change Draft/Ready state, edit PR metadata, or post comments. Markdown is the canonical output. Host-supported inline comments may supplement it only when the reviewed head is the exact local workspace state.

## GitHub Constraints

- GitHub's current repository limits document a 300-file diff limit, 20,000 loadable lines or 1 MB total raw diff, and 20,000 lines or 500 KB for one file: https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits
- The pull-request files REST endpoint documents pagination up to 100 items per page and a maximum response of 3,000 files: https://docs.github.com/en/rest/pulls/pulls#list-pull-requests-files

Treat these links as maintenance sources for the helper constants, not as a reason to trust a diff that the captured evidence marks incomplete.
