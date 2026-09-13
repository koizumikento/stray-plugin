"""Private Windows file creation shared by Studio artifact writers."""

import os
import subprocess
from pathlib import Path


def create_private_windows_file(path: Path) -> None:
    """Create an empty file with a protected current-user-only DACL, before any payload."""
    # Windows PowerShell 5.1 supplies the .NET Framework ACL-aware CreateNew overload.
    # Pass the path as data, never interpolate it into executable PowerShell source.
    script = r"""
$ErrorActionPreference = 'Stop'
$sid = [System.Security.Principal.WindowsIdentity]::GetCurrent().User
$acl = [System.Security.AccessControl.FileSecurity]::new()
$acl.SetOwner($sid)
$acl.SetAccessRuleProtection($true, $false)
$acl.AddAccessRule([System.Security.AccessControl.FileSystemAccessRule]::new(
    $sid, [System.Security.AccessControl.FileSystemRights]::FullControl,
    [System.Security.AccessControl.AccessControlType]::Allow))
$stream = [System.IO.FileStream]::new(
    $env:STRAY_PRIVATE_STAGING_PATH, [System.IO.FileMode]::CreateNew,
    [System.Security.AccessControl.FileSystemRights]::FullControl,
    [System.IO.FileShare]::None, 4096, [System.IO.FileOptions]::None, $acl)
$verified = $false
try {
    $actual = $stream.GetAccessControl()
    $rules = @($actual.GetAccessRules($true, $true, [System.Security.Principal.SecurityIdentifier]))
    if (!$actual.AreAccessRulesProtected -or $rules.Count -ne 1 -or
        $actual.GetOwner([System.Security.Principal.SecurityIdentifier]).Value -ne $sid.Value -or
        $rules[0].IdentityReference.Value -ne $sid.Value -or $rules[0].IsInherited -or
        $rules[0].AccessControlType -ne [System.Security.AccessControl.AccessControlType]::Allow -or
        $rules[0].FileSystemRights -ne [System.Security.AccessControl.FileSystemRights]::FullControl) {
        throw 'Private file ACL verification failed'
    }
    $verified = $true
} finally {
    $stream.Dispose()
    if (!$verified) { [System.IO.File]::Delete($env:STRAY_PRIVATE_STAGING_PATH) }
}
"""
    powershell = Path(os.environ["SystemRoot"]) / "System32/WindowsPowerShell/v1.0/powershell.exe"
    subprocess.run(
        [str(powershell), "-NoProfile", "-NonInteractive", "-Command", script],
        env={**os.environ, "STRAY_PRIVATE_STAGING_PATH": str(path)},
        check=True, capture_output=True, timeout=30,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )
