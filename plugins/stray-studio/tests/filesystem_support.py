"""Platform-aware filesystem assertions; CI must exercise symlink guards."""
import json
import os
import subprocess
from pathlib import Path

import pytest


def make_symlink(link: Path, target: Path | str, *, target_is_directory: bool = False) -> None:
    try:
        link.symlink_to(target, target_is_directory=target_is_directory)
    except OSError as error:
        if os.name != "nt" or getattr(error, "winerror", None) != 1314:
            raise
        reason = "Windows symlink privilege unavailable (WinError 1314)"
        if os.environ.get("STRAY_REQUIRE_SYMLINKS") == "1":
            pytest.fail(reason + "; this CI job requires symlink coverage")
        pytest.skip(reason)


def assert_private_file(path: Path) -> None:
    if os.name != "nt":
        assert path.stat().st_mode & 0o777 == 0o600
        return
    # Read the persisted security descriptor independently of the production writer.
    script = r"""
$ErrorActionPreference = 'Stop'
$sid = [System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value
$acl = [System.IO.File]::GetAccessControl($env:STRAY_TEST_ACL_PATH)
$rules = @($acl.GetAccessRules($true, $true, [System.Security.Principal.SecurityIdentifier]) |
    ForEach-Object { @{sid=$_.IdentityReference.Value; rights=[int]$_.FileSystemRights;
        inherited=$_.IsInherited; type=[int]$_.AccessControlType} })
@{user=$sid; owner=$acl.GetOwner([System.Security.Principal.SecurityIdentifier]).Value;
    protected=$acl.AreAccessRulesProtected; rules=$rules} | ConvertTo-Json -Depth 4 -Compress
"""
    powershell = Path(os.environ["SystemRoot"]) / "System32/WindowsPowerShell/v1.0/powershell.exe"
    result = subprocess.run(
        [str(powershell), "-NoProfile", "-NonInteractive", "-Command", script],
        env={**os.environ, "STRAY_TEST_ACL_PATH": str(path)},
        capture_output=True, text=True, check=True, timeout=30,
    )
    acl = json.loads(result.stdout)
    assert acl["protected"] and acl["owner"] == acl["user"]
    assert acl["rules"] == [{"sid": acl["user"], "rights": 0x1F01FF,
                              "inherited": False, "type": 0}]
