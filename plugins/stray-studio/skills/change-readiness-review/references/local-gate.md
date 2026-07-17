# Local Push Gate

Use this adapter only for an explicit author-side push-readiness decision.

## Establish The Target

1. Resolve the comparison ref in this order:
   - explicit user-provided ref
   - configured upstream of the current branch
   - remote default branch such as `refs/remotes/origin/HEAD`
2. If more than one plausible base would materially change the review, stop and ask for the base instead of guessing.
3. Distinguish the base ref tip from the merge base. Review committed change from `merge-base..HEAD`.
4. Include staged, unstaged, and relevant untracked state because a pushable implementation may depend on work that is not in the outgoing commits.

## Capture

From this skill directory, create an external temporary directory and capture once:

```bash
snapshot_dir=$(mktemp -d)
chmod 700 "$snapshot_dir"
python3 scripts/capture_local_state.py \
  --repo <repository> \
  --base <resolved-base-ref> \
  --snapshot-dir "$snapshot_dir" \
  --name initial
```

The helper records exact OIDs, index state, Git-visible changed paths, raw worktree fingerprints for changed and untracked paths, changed gitlinks, and a canonical snapshot fingerprint. It does not decide findings and does not include file contents in standard output.

When displaying patches for review, use:

```bash
git diff --no-ext-diff --no-textconv -- <paths>
git diff --cached --no-ext-diff --no-textconv -- <paths>
git diff --no-ext-diff --no-textconv <merge-base>..HEAD -- <paths>
```

## Review Decisions

- `READY` requires no blocking finding, no push-relevant dependency left only in staged, unstaged, or untracked state, and no material proof gap.
- `CHANGES_REQUIRED` includes a confirmed defect, missing required artifact, unintended outgoing file, or local-only dependency that would make the pushed commits incomplete.
- `INCOMPLETE` applies when the base cannot be fixed, a changed gitlink has not been reviewed as its own repository, the state cannot be captured safely, or missing evidence could conceal a blocking defect.

Do not use this adapter for generic review of uncommitted work. That request belongs to `reviewer` and has no push-readiness verdict.

## Freshness Check

Immediately before deciding, rerun the same command with `--name final`. Compare every captured field and `snapshot_sha256`.

- If the snapshots match, decide against the sealed initial evidence.
- If they differ, identify the changed surface. Re-review it only when bounded and complete; otherwise return `INCOMPLETE`.
- Remove the entire temporary directory after the decision.

## Trust Boundary

The helper disables external diff, text conversion, fsmonitor integration, optional Git locks, and pagers for the commands it owns. Git's normal changed-path detection can still be affected by repository attributes and filters, so use it only for a trusted repository or inside an appropriate sandbox. Do not describe this as a forensic audit of hidden `assume-unchanged`, `skip-worktree`, filter, or submodule state.
