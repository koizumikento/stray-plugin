# Target Analysis

Read only the route needed for the selected artifact or observation. The entries describe investigation methods, not tested support for every OS, format, or engine.

## Select the route

| Target | First useful evidence | Follow-up and prerequisite |
|---|---|---|
| Web service or running app | The selected screen, recorded actions, scripts, or retained network capture | Use available browser observation or automation for the requested scenario. Inspect the capture tool's limits; visible behavior and network exchanges do not reveal all server internals. Do not fetch recorded URLs without a live request scope. |
| Electron / JavaScript distribution | ASAR or extracted module inventory, source maps, resources, and configuration | Follow renderer to preload, IPC, main process, and native add-ons as applicable. Use an installed format-aware reader or available REA analysis; code inspection need not run the app. Check that packaged and observed builds match. |
| Native executable or library | Container format, sections, symbols, strings, imports, and references | Use available format tools for inventory; use a compatible installed disassembler/decompiler such as Ghidra, IDA, or Hopper for code. Confirm architecture, loader, provider and host support before selecting it. Pseudocode can omit or misrepresent behavior. |
| .NET assembly | Assembly metadata, CIL, resources, and declared native dependencies | Use a compatible managed-code inspector; distinguish ordinary CLI assemblies from NativeAOT, which may require native analysis. Metadata alone does not establish executed behavior. |
| Android APK | Package members, manifest, resources, classes, and references | Check an installed compatible decoder/decompiler, such as Apktool or JADX and its Java prerequisite. Device work additionally needs authorized device access and suitable tools such as adb; package inspection does not prove device behavior. |
| Other archive / package | Members, content digests, resource metadata, and nested artifacts | Inventory without extraction where possible; inspect only relevant members with a format-aware reader. Validate destination paths and symlink handling before extraction so entries cannot escape the selected directory. |
| Firmware image | Region signatures, offsets, format and embedded-resource inventory | Use compatible installed format tools, including Binwalk or Unblob when appropriate to the host. Extract only when needed and authorized, then pass identified native code to its analysis route. Image analysis does not establish boot or hardware behavior. |
| Version comparison | Exact artifact identities and comparable inventory, function or observation records | Keep architecture, analysis settings and observation scenarios comparable. Missing pages or different scope prevents an absence/equivalence claim; a static change is a candidate explanation until behavior is corroborated. |

## Work with optional REA

1. Prefer the connected server's advertised tool list and input schemas, or an existing CLI's help. Select capabilities by the target; names and arguments in repository main can differ from the installed release. Do not require REA diagnostics or native engines for unrelated supported inspection.
2. Record the active target and provider when sessions are used. Reuse matching evidence; do not open duplicate sessions or disturb manually opened tools. Follow the provider's actual lifecycle and close only sessions created for the task.
3. Use returned Evidence IDs and retained summaries/pages where advertised. If the server has no retained-reference capability, preserve complete output within the local resource budget and its limitations. Do not fabricate a REA record for shell or browser results.
4. If connection or a capability fails, identify the blocker before proposing repair. A skill installation, configuration file, or successful diagnostic does not establish tool availability in the current agent. Review concrete repair paths and effects under existing authorization; restart/reconnect only when necessary. Do not install REA, engines, or unrelated prerequisites merely to make every route available.

## Preserve evidence identity

Record artifact paths, versions and digests when available; for code, record function/address and analysis settings. For runtime evidence, record instance/build, actions, timing and capture boundaries. Do not reconcile static and runtime results solely from a similar filename when builds disagree. Label user-supplied path mappings and inferred correspondences as assumptions.

For oversized output, select a stable section/page and retain the parent identity. Do not treat a preview as complete JSON or claim complete search coverage from one page. When a question remains unanswered, request the specific missing evidence, rather than repeating a broad analysis or claiming complete recovery.
