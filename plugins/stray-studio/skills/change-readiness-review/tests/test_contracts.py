from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[5]
STUDIO_ROOT = REPO_ROOT / "plugins" / "stray-studio"
SKILL_ROOT = STUDIO_ROOT / "skills" / "change-readiness-review"


def test_skill_has_focused_trigger_and_all_references() -> None:
    skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert skill.startswith(
        '---\nname: "change-readiness-review"\ndescription: "Use when'
    )
    for phrase in (
        "LOCAL_PUSH",
        "PR_REVIEW_REQUEST",
        "READY",
        "CHANGES_REQUIRED",
        "INCOMPLETE",
        "state-sealed readiness decision",
        "Do Not Use For",
        "never convert this gate into a repair loop",
    ):
        assert phrase.lower() in skill.lower()
    for name in (
        "local-gate.md",
        "pull-request-gate.md",
        "finding-policy.md",
        "risk-modules.md",
        "meta-sanity-pass.md",
        "output-contract.md",
    ):
        assert (SKILL_ROOT / "references" / name).is_file()
        assert f"references/{name}" in skill


def test_helpers_and_metadata_are_packaged_with_the_skill() -> None:
    for name in (
        "_snapshot_common.py",
        "capture_local_state.py",
        "capture_pr_state.py",
    ):
        assert (SKILL_ROOT / "scripts" / name).is_file()
    metadata = (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
    assert 'display_name: "Change Readiness Review"' in metadata
    assert "$change-readiness-review" in metadata
    pull_reference = (SKILL_ROOT / "references" / "pull-request-gate.md").read_text(
        encoding="utf-8"
    )
    assert "--workspace-root <current-workspace>" in pull_reference
    assert "linked closing Issues" in pull_reference


def test_reviewer_routes_explicit_readiness_to_the_new_skill() -> None:
    reviewer = (STUDIO_ROOT / "skills" / "reviewer" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    code_review = (
        STUDIO_ROOT / "skills" / "reviewer" / "references" / "code-review.md"
    ).read_text(encoding="utf-8")
    assert "change-readiness-review" in reviewer
    assert "change-readiness-review" in code_review
    assert "Do not delegate by default" in code_review
    assert "--no-ext-diff --no-textconv" in code_review


def test_manifest_and_readme_discover_the_new_skill() -> None:
    manifest = json.loads(
        (STUDIO_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    assert manifest["version"] == "0.1.7"
    assert "change-readiness" in manifest["interface"]["longDescription"]
    prompts = manifest["interface"]["defaultPrompt"]
    readiness_prompts = [
        value for value in prompts if "exact local Git or open PR state" in value
    ]
    assert len(readiness_prompts) == 1
    assert len(readiness_prompts[0]) <= 128
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "| `change-readiness-review` |" in readme
    assert "change-readiness-review/tests/" in readme


def test_routing_cases_cover_intended_and_near_miss_prompts() -> None:
    routing = json.loads(
        (
            REPO_ROOT
            / "plugins"
            / "stray-skillops"
            / "skills"
            / "skill-routing-validator"
            / "references"
            / "routing-cases.json"
        ).read_text(encoding="utf-8")
    )
    cases = {value["id"]: value for value in routing["cases"]}
    assert cases["studio-change-readiness-local-push"]["expect"] == [
        "change-readiness-review"
    ]
    assert cases["studio-change-readiness-pr-rerequest"]["expect"] == [
        "change-readiness-review"
    ]
    assert cases["studio-general-code-review-not-readiness"]["expect"] == ["reviewer"]
    assert (
        "change-readiness-review"
        in cases["studio-general-code-review-not-readiness"]["reject"]
    )
    assert set(cases["studio-review-fix-then-readiness"]["expect"]) == {
        "reviewer",
        "change-readiness-review",
    }
