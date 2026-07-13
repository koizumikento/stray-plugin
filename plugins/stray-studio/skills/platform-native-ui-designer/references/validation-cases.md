# Validation Cases

Use these cases to verify that `platform-native-ui-designer` owns platform-specific interface specification work from user-authored notes attributed to current official Apple design pages and stays out of product strategy, review, implementation, extraction, branding, and App Store policy.

## Acceptance Boundary

Trigger this skill when the user already knows the feature or flow they need and wants concrete UI decisions for Apple platforms grounded in their own notes about current official pages, with source URLs and user-reported access dates.

Do not trigger it when the primary deliverable is:

- a product strategy, feature brief, or PRD
- findings-first critique of an existing artifact
- source code or a working application
- extraction or summary of an Apple page
- brand identity or marketing assets
- App Store policy or legal analysis

## Positive Cases

| Prompt | Expected behavior | Expected outcome |
| --- | --- | --- |
| "Apple HIGに沿って、iPhoneのアカウント削除フローのUI仕様を作って" | Trigger | Requests the supported OS baseline, gives the smallest relevant category links, and requests user-authored source notes before producing the specification. |
| "対象OS、出典URL、閲覧日付きで添付した自分のメモを使って、iPadのsidebarとdetailの画面構成を設計して" | Trigger | Uses the supplied baseline and notes without requesting them again and covers resizing, multitasking, pointer and keyboard use, empty selection, and compact adaptation. |
| "macOSの編集アプリでtoolbar、menu、inspectorの役割を整理した仕様が欲しい" | Trigger | Requests the supported OS baseline and missing user-authored source notes before producing a macOS-specific command and window model. |
| "watchOSで服薬記録を数秒で完了できるフローを設計して" | Trigger | Requests the supported OS baseline and missing user-authored source notes before designing the short watchOS task. |
| "visionOSの製品レビュー体験をwindowとvolumeのどちらで始めるべきか仕様にして" | Trigger | Requests the supported OS baseline and user-authored spatial-design source notes before making scene, input, comfort, and transition decisions. |
| "同じ承認フローをiPhone、iPad、Mac向けに設計し分けて" | Trigger | Requests the OS baselines and platform-specific source notes before creating a shared task model with explicit navigation, input, window, and adaptation differences. |

## Negative Cases

| Prompt | Expected behavior | Route |
| --- | --- | --- |
| "この新機能を作るべきか市場調査してPRDを書いて" | Do not trigger | `product-designer` |
| "このiOS画面のスクリーンショットをレビューして問題を列挙して" | Do not trigger | `reviewer` |
| "この仕様をSwiftUIで実装してSimulatorで動かして" | Do not trigger as primary owner | `fullstack-app-builder` for current-repository app work or a specialized available iOS or SwiftUI builder |
| "Apple DesignのページをMarkdownに整理して" | Do not trigger | Do not hand the Apple-domain extraction to another skill; request user-authored notes or decline. |
| "Appleっぽいブランドとアプリアイコンを作って" | Do not trigger | `brand-designer` or an asset skill |
| "このアプリがApp Store審査で拒否されないと保証して" | Do not trigger | App Store policy or compliance workflow; do not guarantee approval |
| "WebとAndroidを含む共通デザインシステムを作って" | Do not trigger | Generic cross-platform product or design workflow |

## Overlap Cases

| Prompt | Primary owner | Expected sequencing |
| --- | --- | --- |
| "HIGに沿ってiOS設定画面を設計してSwiftUIで実装して" | UI designer, then `fullstack-app-builder` or a specialized iOS or SwiftUI builder | Produce and hand off the platform UI specification before code implementation. |
| "このSwiftUI画面がHIGに沿っているかレビューして直して" | `reviewer`, then implementation skill | Reviewer owns findings; user-authored notes attributed to official Apple pages may support findings; implementation skill applies confirmed fixes. |
| "iPad版の機能範囲を決めてから画面仕様にして" | `product-designer`, then UI designer | Settle product scope first, then create the platform-specific interface specification. |
| "Appleの最新デザイン変更を調べて、この既存フローへの影響を教えて" | No automated Apple-domain research | Request user-authored notes with exact source URLs and access dates; then use `reviewer` only when findings against a concrete artifact are requested. |

## Pass Criteria

- The output names the target platform, OS baseline, device or window context, and input methods.
- User-authored source notes include user-reported page titles, exact attributed official URLs, and user-reported access dates.
- Japanese-to-English fallback is disclosed.
- The output separates guidance reported in user-supplied notes, design recommendation, and user or repository constraint.
- The design covers material states, adaptation, accessibility, localization, and recovery.
- Multi-platform work does not apply one platform's conventions indiscriminately to another.
- The output is an interface specification, not a PRD, findings-first audit, code change, web extraction, or branding artifact.
- No Apple content corpus, downloadable asset, crawler, or long copied passage is created.
- The skill does not ask the user to copy, upload, or transmit Apple page content.
- The skill does not automatically access or retrieve content from Apple domains.
- The skill does not hand Apple-domain retrieval or content copying to another skill, agent, connector, or tool.
- The output does not promise Apple endorsement, App Store approval, or complete compliance.
