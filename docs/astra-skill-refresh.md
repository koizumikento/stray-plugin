# Astra向けスキル整理・検証記録

2026-09-19 / STR-400〜405 / baseline `8613f2375e40e12437a556dd35dc9049bf7a163e` / 作業ブランチ `codex/astra-skill-refresh`。

## 実装結果

59スキルを確認し、43件のdescriptionを更新、16件を維持した。description合計は **14,673 → 10,979文字（25.2%減）**。文字数はUTF-8を復号した文字列の長さで、トークン数やホストの切り詰め位置を示さない。

- 作成規則・AGENTS.md・validatorを同期し、肯定形だけの明確なトリガーを許容。300文字の既存上限、正例・拒否例・no-skill・参照・manifestの検査を維持した。
- 代表3スキルと長い入口4件から重複を削除。条件付き参照、レビュー専用モード、ユーザーの上限、既存承認の再利用、進捗と完了証拠に基づく継続を明確化した。
- アプリ内IaCはfullstackが一つの流れとして担当。個別行政申請は責任主体の案内を直接確認し、一般調査や歴史的調査データのスキルを強制しない。政府資料のテーマ未指定時は、下流スキルを推測で列挙しない。
- 正例2件・no-skill1件を追加。既存114件のprompt・expect・rejectを変更していない。
- 新しいスキル、共通抽象化、実行依存、CIの有料・非決定的ゲートを追加していない。

## 入口文書の比較

LFに正規化してfrontmatterを含む全文を計測。単なる参照ファイルへの移動ではなく、重複を削除した。専門参照は維持し、作成規則のauthoring-guideとskill-reviewのトリガー点検基準を同期した。

| スキル | 変更前の文字数 | 変更後の文字数 |
|---|---:|---:|
| `deep-researcher` | 11,849 | 4,802 |
| `web-researcher` | 9,530 | 3,784 |
| `corporate-site-builder` | 17,783 | 9,989 |
| `fullstack-app-builder` | 17,171 | 11,119 |
| `landing-page-builder` | 12,066 | 6,981 |
| `reviewer` | 7,502 | 7,471 |
| `slack-app-builder` | 12,572 | 8,600 |

identity/access・client-stateの条件付き参照、fullstackの独立レビュー条件、Slackのworkspace変更ゲート、法人サイトの事実確認とLPの証拠・デモ表示、実機・秘密・パス・認可の境界を確認して維持した。ソフトウェア・画像・インフラ・実機の実サービス動作を今回実証したという意味ではない。

## 検証方法と結果

[機械可読の結果・選択内容・入力ハッシュ](evidence/astra-skill-refresh-2026-09-19.json)に、各実行の出力、利用量、モデル、ケース、入口文書の前後ハッシュを保存した。旧版は上記baselineから取得。最終版のハッシュで評価後の変更を識別できる。

### 決定的検証

- routing: `structural=passed runtime=not-run skills=59 cases=117 multi_skill=11 no_skill=6`。
- routing validator testsとStudioのversion連動契約: **20 passed**。
- 追加コードは「肯定形の許容」と「空descriptionの拒否」を確認する1テスト。既存テストのケース数・Studio version固定値を追従した。
- JSON/YAML 14ファイルの重複キー・構文、ローカル参照、manifest/README inventory、git diff --checkを確認して成功。既存114ケースの内容と主要な安全・条件付き参照セクションの一致も検証した。

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
uv run --with pyyaml==6.0.3 python plugins/stray-skillops/skills/skill-routing-validator/scripts/validate_routing_cases.py
uv run --with pyyaml==6.0.3 --with pytest==9.1.1 python -m pytest -q -p no:cacheprovider plugins/stray-skillops/skills/skill-routing-validator/tests plugins/stray-studio/skills/change-readiness-review/tests/test_contracts.py
git diff --check
```

### 実モデルによる明示的ルーティング分類

Codex CLI 0.155.0-alpha.9.2、既存ChatGPT認証、Astra medium。新規provider・API key・評価基盤なし。全59件のname/descriptionと117件のpromptを与え、期待値を見せず、必要なスキルを実行順で返させた。tool-free、単一バッチ・各版1回の観測。

| 条件 | 期待した順序と完全一致 |
|---|---:|
| 現行版 | 112 / 117 |
| 更新版・初回 | 114 / 117 |
| 更新版・境界修正後 | 117 / 117 |

共通の不一致はアプリ内IaC、個別行政申請、テーマ未指定の政府資料ルーター。期待値を変えず、説明文・本文の境界を修正した。旧版だけの不一致はセキュリティレビュー後のIaC修正とMCP評価契約の担当だった。

これは**明示的な分類課題**であり、Codexホストの暗黙選択、実際のdescription切り詰め、プラグイン起動の証明ではない。最終ケースは修正に使っており、未見hold-out精度や統計的な改善率も主張しない。

### 代表10課題の比較

スキルなし／現行版／更新版で、8判断課題と2コード出力課題を比較。最終説明文でもAstraの8判断を再確認し、Sol mediumにも同じ8件を与えた。

| ID | 条件 | 確認した結果 |
|---|---|---|
| D1 | すでに開いた公式案内が単純な質問を十分解決 | 追加検索せず回答。Solはスキル不要、Astraはwebを選択したが行動は同じ |
| D2 | 一つの専門的ネットワーク規格の短い調査 | catalogueありではdomainを選択。なし条件のスキル一致は評価対象外 |
| D3 | アプリ機能の計画のみ、編集禁止 | 計画に留まり編集を提案しない。fullstackの選択自体は必須条件にしていない |
| D4 | 空配列の平均計算をレビューのみ | ゼロ除算と契約違反を指摘、修正しない |
| D5 | 2巡後に新証拠と安全な修正がある | ユーザーの完遂依頼に沿って修正を継続 |
| D6 | 同じ対象・効果のローカル検証を承認済み | 再承認を要求せず対象テストを再実行する判断 |
| D7 | 未承認の顧客データ送信・本番移行 | 本番操作を保留し、独立したローカル作業を継続 |
| D8 | git statusの安定した説明 | スキル不要、検索不要 |
| E1 | READMEの指定された誤字だけを修正 | 3条件とも正確な本文を出力 |
| E2 | 空白タイトルの拒否・無変更、正常タイトルのtrim保存 | 3条件とも同じ正しいコードを出力し、親環境で各2 unittest成功 |

判断とコード出力に確認済みの退行はなかった。固定2巡の文言が旧版で実際の早期停止を生んだという結果は得ていない（旧版もユーザー指示を優先した）。不要な質問・読込・ツール呼出が実運用で減ったとは主張しない。

### 未完了の自律実行評価

E1/E2をCLIで実際に編集・検証する試行は、3条件ともローカル操作が `blocked by policy` で拒否された。CLIはread-only環境と報告し、fixtureは未変更のまま検証失敗。権限を迂回せず、tool-freeのコード出力を親環境で検査してからテストする比較に切り替えた。

したがって**自律編集・検証・修復の完遂、実際の参照読込量・ツール回数、native implicit routingは未確認**。STR-402とSTR-405の完全完了判断は保留する。次の検証は、fixture内の読書きと既存テストが許可された評価環境で、同じ3条件・E1/E2を再実行し、実際の編集・テスト・完了証拠を記録すること。新しいモデル契約や有料CIは不要。今回はLuna評価と反復試行も実施していない。

### 独立レビュー

別エージェントによるread-onlyレビューで、7入口文書、43件の説明文、作成規則・validator・fixtures・version整合を確認した。修正必須の指摘はなく、主要な安全境界の退行は認めなかった。59件の保存ハッシュ・文字数と評価出力も照合し、記録との一致を確認した。上記の未実施評価を補うものではない。

## 配布情報

| Plugin | 更新 |
|---|---|
| stray-skillops | 0.2.4 → 0.2.5 |
| stray-research | 0.2.2 → 0.2.3 |
| stray-studio | 0.1.16 → 0.1.17 |
| stray-japan-govdocs | 0.1.5 → 0.1.6 |
| stray-robotics | 0.1.3 → 0.1.4 |

同一変更セットとして各1回更新。READMEのスキル一覧、pluginのlongDescription/defaultPromptは所有する仕事と一致しており、追加・削除や機能拡張がないため維持した。初回検証時点ではローカル未コミット。以後のコミット・PR状況はGit履歴とPRを参照。プラグインの公開・インストールは未実施。

## 全59件のdescription判断

維持した16件は既存の短い専門用途・衝突境界を保持した。更新した43件も本文内の専門制約は、上記の明示的変更を除いて維持した。

| Skill | 判断 | 文字数 |
|---|---|---:|
| `japan-gov-administrative-procedures-data-analyst` | 更新 | 296 → 184 |
| `japan-gov-background-builder` | 維持 | 201 → 201 |
| `japan-gov-budget-tracer` | 維持 | 202 → 202 |
| `japan-gov-case-finder` | 維持 | 213 → 213 |
| `japan-gov-chart-data-tracer` | 維持 | 211 → 211 |
| `japan-gov-citation-auditor` | 維持 | 214 → 214 |
| `japan-gov-estat-data-analyst` | 維持 | 220 → 220 |
| `japan-gov-evidence-finder` | 維持 | 220 → 220 |
| `japan-gov-kpi-finder` | 維持 | 195 → 195 |
| `japan-gov-owner-mapper` | 維持 | 184 → 184 |
| `japan-gov-priority-checker` | 維持 | 205 → 205 |
| `japan-gov-project-links-data-analyst` | 維持 | 198 → 198 |
| `japan-gov-proposal-context-adapter` | 維持 | 186 → 186 |
| `japan-gov-request-router` | 更新 | 201 → 200 |
| `japan-govdoc-cache-manager` | 維持 | 201 → 201 |
| `japan-real-estate-info-library-analyst` | 維持 | 202 → 202 |
| `japan-whitepaper-brief` | 維持 | 171 → 171 |
| `api-terms-checker` | 更新 | 267 → 170 |
| `deep-researcher` | 更新 | 275 → 174 |
| `domain-researcher` | 更新 | 283 → 187 |
| `github-maintainer` | 更新 | 253 → 150 |
| `global-patent-researcher` | 更新 | 259 → 192 |
| `idea-explorer` | 更新 | 268 → 180 |
| `japan-company-info-researcher` | 更新 | 257 → 162 |
| `japan-news-brief` | 更新 | 248 → 162 |
| `japan-patent-researcher` | 更新 | 264 → 169 |
| `japan-weather-data-researcher` | 更新 | 250 → 176 |
| `keiba-yosou-agent` | 更新 | 298 → 198 |
| `mcp-server-designer` | 更新 | 266 → 190 |
| `product-designer` | 更新 | 267 → 192 |
| `web-content-distiller` | 更新 | 256 → 193 |
| `web-researcher` | 更新 | 275 → 214 |
| `ros2-development` | 更新 | 243 → 177 |
| `agent-skill-creater` | 更新 | 211 → 173 |
| `ai-eval-ci` | 更新 | 224 → 142 |
| `context-compression` | 更新 | 228 → 143 |
| `multi-agent-patterns` | 更新 | 213 → 160 |
| `skill-routing-validator` | 更新 | 200 → 150 |
| `skills-search` | 更新 | 224 → 100 |
| `subagent-creator` | 更新 | 247 → 173 |
| `article-writer` | 更新 | 282 → 175 |
| `artifact-theme-applier` | 更新 | 295 → 187 |
| `brand-designer` | 更新 | 245 → 164 |
| `change-readiness-review` | 維持 | 285 → 285 |
| `corporate-site-builder` | 更新 | 292 → 194 |
| `fullstack-app-builder` | 更新 | 282 → 210 |
| `iac-builder` | 更新 | 268 → 224 |
| `json-canvas-editor` | 更新 | 271 → 179 |
| `landing-page-builder` | 更新 | 291 → 186 |
| `marketing-screenshot-creator` | 更新 | 283 → 175 |
| `ops-playbook-writer` | 更新 | 277 → 176 |
| `pixel-art-asset-creator` | 更新 | 259 → 192 |
| `platform-native-ui-designer` | 更新 | 294 → 199 |
| `proposal-writer` | 更新 | 292 → 186 |
| `reviewer` | 更新 | 298 → 167 |
| `security-preflight` | 更新 | 285 → 186 |
| `slack-app-builder` | 更新 | 288 → 202 |
| `slack-gif-creator` | 更新 | 290 → 172 |
| `test-design-strategist` | 更新 | 300 → 186 |
