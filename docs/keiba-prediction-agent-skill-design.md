# 競馬予想エージェントスキル設計メモ

作成日: 2026-06-06

## 結論

競馬予想エージェントは `plugins/stray-research/skills/keiba-yosou-agent/` に置くのが自然。主目的は「日本競馬のレースを、公開・認可データとユーザー提供データから分析し、買い目ではなく根拠付きの確率・期待値・リスクを出す」ことにする。

スキルは予想の断言やギャンブル助長ではなく、分析手順、データ品質確認、確率推定、オッズとの比較、責任ある利用の明示を強制する。スクレイピング前提の実装は避け、JRA-VAN Data Lab.、JRA公式ページ、地方競馬公式CSV、ユーザー提供CSV/PDF/画像、利用許諾済みデータを優先する。

## 調査メモ

### 一次データ候補

- JRA公式の競馬メニューには、出馬表、オッズ、過去のレース結果、競走馬検索、騎手・調教師データなどがまとまっている。
- JRA-VAN Data Lab. はリアルタイム・過去データを取得する競馬ソフト向けサービス。JV-Link 経由で JV-Data を取得し、レース情報、競走馬情報、馬体重、オッズなどのリアルタイム情報も対象になる。月額利用、利用キー、ActiveX COM 依存があるため、汎用Web APIとして扱わない。
- 地方競馬情報サイトはデータダウンロード機能を提供している。2026-05-21更新の説明書では、ZIP内CSVとして出馬表、払戻金、レース一覧、オッズを取得でき、当日ファイルは約2分ごと、月次ファイルは夜間に更新される。
- netkeiba は大規模な競馬DBとして有用だが、データ提供元のライセンス表記があり、利用規約では私的利用範囲外の複製・販売・公開や商用利用に制限がある。スキルは netkeiba の自動収集を標準手順にしない。

### 予想で扱う主要特徴量

- レース条件: 競馬場、芝/ダート、距離、右左回り、内外回り、馬場状態、天候、クラス、頭数、枠順。
- 馬の能力: 近走成績、着差、走破時計、上がり、通過順、斤量、馬体重と増減、休み明け、距離・馬場・競馬場適性。
- 人と陣営: 騎手、調教師、乗り替わり、厩舎成績、ローテーション、輸送、調教コメントがある場合の扱い。
- 血統: 種牡馬、母父、芝/ダート適性、距離適性、馬場悪化耐性。ただし過剰解釈を避ける。
- 市場情報: 単勝オッズ、人気、オッズ推移、直前変動、票数またはプール情報が取れる場合の市場確率。
- 直前情報: 馬体重、返し馬、パドック、取消・除外、馬場変更。取得時刻を必ず明記する。

### 分析方針

- まずレース単位で「勝率/複勝率の主観推定」と「市場オッズから見た暗黙確率」を分ける。
- 買い目候補は、予想確率が市場確率を十分上回る場合だけ「期待値候補」として出す。
- オッズは締切直前に大きく動く。日本競馬の中間オッズ研究では、最終局面のオッズ変化に情報が含まれる可能性が示されているため、発走直前でない予想には鮮度警告を付ける。
- 単勝、複勝、馬連、ワイド、三連系では不確実性と必要的中率が違うため、券種ごとにリスクを分けて説明する。
- 回収率を語る場合は、控除率、サンプルサイズ、締切オッズ、購入制約を明示する。

### 券種と性格

JRA公式の初心者向け資料では、馬券は単勝、複勝、応援馬券、枠連、馬連、馬単、ワイド、3連複、3連単、WIN5の10種類と説明されている。スキルでは券種を「当てやすさ」ではなく「予想仮説に合うか」で選ばせる。

- 単勝: 1着馬を当てる。勝ち切る馬の評価に向く。市場確率との比較がしやすい。
- 複勝: 通常は3着以内を当てる。軸候補の堅さを見る券種だが、人気馬では妙味が薄くなりやすい。
- 応援馬券: 単勝と複勝を同時に買う形式。ファン用途寄りで、期待値分析では単勝・複勝に分解して扱う。
- 枠連: 1着・2着の枠番号の組合せ。枠単位なので、同枠複数頭の扱いを確認する。
- 馬連: 1着・2着の馬番号の組合せ。順不同。相手関係の読みが必要。
- 馬単: 1着・2着を着順通りに当てる。勝ち馬の確信が必要で、馬連より分散が大きい。
- ワイド: 3着以内に入る2頭の組合せ。軸馬と相手の安定性を見るのに向くが、多点化するとトリガミになりやすい。
- 3連複: 1着から3着の3頭の組合せ。順不同。相手の範囲設定が重要。
- 3連単: 1着から3着を着順通りに当てる。高配当になりやすいが、点数と分散が大きい。
- WIN5: JRA指定5レースすべての1着馬を当てる。インターネット投票・UMACA投票限定。単レース予想より、対象5レース全体の点数設計が主問題になる。

JRAの払戻率は投票法ごとに違う。2014年6月7日以降の設定では、単勝・複勝80.0%、枠連・馬連・ワイド77.5%、馬単・3連複75.0%、3連単72.5%、WIN5 70.0%と案内されている。スキルは、払戻率が低い券種を「夢があるから推す」のではなく、必要な予想精度と分散が上がるものとして扱う。

### 買い方の定石

JRAの用語辞典や投票マニュアルには、ボックス、ながし、フォーメーション、オッズ投票、予算入力による自動配分などが出てくる。スキルでは以下のように買い方を分類する。

- 1点買い: 最も仮説が明確。外れやすいが、根拠と期待値検証がしやすい。
- 複数点均等買い: 予想候補を広げる基本形。各点の期待値が薄いなら点数を増やしても改善しない。
- ボックス: 選んだ馬の全組合せを買う。抜け漏れを減らすが、点数が急増する。3連系では特にトリガミと過剰投資を確認する。
- ながし: 軸馬を決め、相手を複数選ぶ。軸の信頼度が高いときに向く。軸が崩れると全滅する。
- マルチ: 馬単・3連単などで軸馬の着順違いも拾う。保険になるが点数が増えるため、軸の勝ち切り評価が弱い場合の逃げ道にしない。
- フォーメーション: 1着候補、2着候補、3着候補を層で分ける。3連系の点数を絞る主力手法。各層の理由を明記させる。
- ダッチング/均等払戻型: どれが当たっても払戻額が近くなるよう金額配分する考え方。JRAダイレクトの操作マニュアルにも予算金額から概ね均一に配分する機能がある。オッズ変動と最低購入単位で結果がずれる点を明記する。
- 見送り: 最重要の選択肢。期待値が不明、データが古い、直前情報が未確認、オッズが下がりすぎた場合は買わない判断を標準にする。

### 券種選択の実務ルール

- 軸馬の勝ち切りに強い根拠がある: 単勝、馬単、3連単1着固定を検討する。
- 軸馬の複勝圏は堅いが勝ち切りまでは不明: 複勝、ワイド、3連複軸ながしを検討する。
- 上位拮抗で順序に自信がない: 馬連、ワイド、3連複を優先する。
- 人気馬を疑い、相手候補に穴がいる: ワイド、馬連、3連複で相手評価を整理する。
- 3着候補が広い: 3連単より3連複、またはフォーメーションで3着層だけ広げる。
- オッズ妙味がない: 券種を変えて無理に買わず、見送りを第一候補にする。

### 資金管理と検証

- スキルは投票金額を積極的に出さない。ユーザーが希望した場合も、娯楽予算内、損失上限、1レース上限、1日上限を先に確認する。
- フラットベットは、各候補を同額または同じ単位で評価するため検証しやすい。初心者向けのデフォルトにしやすい。
- Kelly基準は理論上、推定確率とオッズから資金配分を計算するが、確率推定の誤差を強く増幅する。スキルに入れる場合は「参考計算」か「fractional Kelly相当の上限管理」に留め、断定的な資金配分にしない。
- 追い上げ、倍賭け、負けを取り戻す前提の資金管理は扱わない。依存リスクと破綻リスクが高い。
- レース後検証では、的中/不的中だけでなく、締切オッズ、想定確率、直前変更、見送り条件、買い目点数、トリガミを記録する。

### ガードレール

- 「必ず当たる」「堅い利益」「資金を増やせる」といった表現を禁止する。
- 20歳未満の馬券購入を前提にした助言をしない。JRA FAQでは馬券購入は20歳以上と案内されている。
- 依存・のめり込み対策を短く入れる。JRAはギャンブル障害に関する入場制限制度などを案内している。
- 個人の資金状況に踏み込んだ金融助言にしない。投票金額は原則出さず、出す場合も上限・損失許容・見送りを優先する。
- データ取得は利用規約・ライセンス・robots・ログイン/課金条件を確認し、禁止または不明なら取得しない。

## スキル設計

### 推奨名

`keiba-yosou-agent`

日本語リクエストの「競馬予想エージェント」を維持しつつ、スキル命名規則に合わせる。

### 配置

`plugins/stray-research/skills/keiba-yosou-agent/`

理由: 競馬予想は、コード生成よりも、現在のデータ確認、根拠付き分析、予測の不確実性整理が中心。既存の `stray-research` の「research and analysis」面に合う。

### フロントマター案

```yaml
---
name: "keiba-yosou-agent"
description: "Use when the user wants Japanese horse racing race analysis, probability estimates, value checks, or betting-ticket candidate reasoning from official, licensed, or user-provided data. Do not use for guaranteed-profit claims, gambling advice for minors, scraping that violates site terms, or fully automated wagering."
---
```

### `SKILL.md` の骨子

```markdown
# Keiba Yosou Agent

Analyze Japanese horse racing races with a cautious, evidence-first posture. Produce probability-oriented race notes, value checks, and risk-aware candidate tickets from official, licensed, or user-provided data.

## Do Not Use For

- Guaranteed-profit or "sure win" claims
- Advice to minors or users who cannot legally buy betting tickets
- Automated wagering, account operation, or bypassing site access controls
- Scraping or redistribution that violates source terms
- Professional financial, legal, or addiction-health advice

## Workflow

1. Scope the race:
   - Identify JRA/NAR, race date, racecourse, race number/name, surface, distance, class, and data timestamp.
   - If live/current data is needed, browse or request user-provided source files instead of using memory.
2. Verify source permissions:
   - Prefer official pages, JRA-VAN/JV-Data where available, NAR CSV, or user-provided files.
   - Do not automate collection from sources with unclear or restrictive terms.
3. Normalize the field:
   - Build a table of runners, frame/horse number, jockey, trainer, weight, body weight, odds, recent form, and scratches.
   - Mark missing or stale fields explicitly.
4. Analyze contenders:
   - Evaluate race fit, recent performance, pace scenario, surface/distance fit, jockey/trainer changes, draw, weight, and condition.
   - Separate evidence from inference.
5. Estimate probabilities:
   - Convert available odds to market-implied probabilities when useful.
   - Produce cautious subjective win/place probability tiers, not false precision.
6. Check value:
   - Compare estimated probability with market probability.
   - Recommend "見送り" when edge is unclear or data is stale.
7. Select ticket structure only if requested:
   - Match the wager type to the prediction hypothesis.
   - Count combinations before suggesting any box, wheel, multi, or formation.
   - Flag trifecta/WIN5 and other high-variance tickets as optional, not default.
8. Output:
   - Lead with top contenders and uncertainty.
   - Include data timestamp, source names, confidence, and responsible-use note.

## Output

- Race summary with timestamp
- Contender table or ranked tiers
- Key positives/negatives by horse
- Probability/value notes
- Optional conservative ticket candidates, clearly marked as not guaranteed
- Data gaps and recheck timing

## Guardrails

- Never promise profit or certainty.
- Never advise under-20 betting.
- Keep stake sizing out unless the user asks; even then, frame as risk control, not income planning.
- Recheck odds, scratches, horse weight, weather, and going near post time.
- Cite or name all sources used.
```

### 追加リソース設計

- `references/source-guide.md`
  - JRA公式、JRA-VAN、NAR CSV、netkeiba、JBIS等の使い分け。
  - 取得可否、規約確認、タイムスタンプ、認可済みデータ優先の判断。
- `references/analysis-checklist.md`
  - レース条件、馬、騎手・調教師、血統、市場、直前情報のチェックリスト。
  - オッズと予想確率を分ける手順。
- `references/output-formats.md`
  - 通常予想、重賞予想、地方競馬予想、レース後検証の出力テンプレート。
- `references/betting-structure-guide.md`
  - 券種、ボックス、ながし、マルチ、フォーメーション、ダッチング、見送り条件、点数計算、トリガミ警告。

初期版では `scripts/` は不要。データ整形のニーズが固まってから、JRA-VANやNAR CSV専用パーサーを追加する。

### 出力フォーマット案

```markdown
## レース概要
- 対象:
- データ時刻:
- ソース:
- 馬場/天候:

## 印と確率レンジ
| 印 | 馬番 | 馬名 | 勝率レンジ | 複勝圏レンジ | 根拠 | 不安材料 |

## 市場との比較
| 馬番 | 馬名 | 単勝オッズ | 市場確率目安 | 評価 | メモ |

## 買い目候補
- 券種:
- 構造:
- 点数:
- 本線:
- 抑え:
- 見送り条件:

## 資金・リスク
- 金額助言:
- トリガミ注意:
- 高分散注意:

## 再確認
- 発走前に確認する情報:
- データ不足:
```

## 実装時の判断

1. まず `SKILL.md` と `references/` 3本で作る。
2. `agents/openai.yaml` は表示メタデータが必要なら追加する。既存スキルには入っているものが多いので、追加推奨。
3. `plugins/stray-research/.codex-plugin/plugin.json` は、競馬予想スキルを追加すると実用面の発見範囲が広がるため、`longDescription` と `defaultPrompt` に1行追加するのが妥当。
4. JSON編集後は AGENTS.md の検証コマンドで marketplace と各 plugin.json を検証する。

## 主要ソース

- JRA 競馬メニュー: https://www.jra.go.jp/keiba/index.html
- JRA-VAN Data Lab. システム概要: https://developer.jra-van.jp/t/topic/49
- 地方競馬データダウンロード機能説明書: https://www.keiba.go.jp/pdf/manual/data_pdf_manual.pdf
- netkeiba database: https://en.netkeiba.com/db/
- netkeiba Terms and Conditions: https://en.netkeiba.com/info/kiyaku.html
- JRA 馬券購入年齢FAQ: https://www.jra.go.jp/faq/pop03/1_2.html
- JRA ギャンブル障害への対応: https://www.jra.go.jp/news/other/izon2.html
- JRA 馬券の種類: https://www.jra.go.jp/kouza/beginner/baken/
- JRA 競馬用語辞典 投票関係: https://www.jra.go.jp/kouza/yougo/c10050_list.html
- JRA 2026 Beginners Book: https://www.jra.go.jp/kouza/beginner/seminar/pdf/beginnersbook2026.pdf
- JRA ダイレクト操作マニュアル: https://www.jra.go.jp/dento/direct/instructions/manual/pdf/direct_manual_sp_pc.pdf
- JRA 勝馬投票法ごとの払戻率: https://jra.jp/news/other/20140303.html
- Kelly Bets and Single-Letter Codes: https://arxiv.org/abs/2104.14277
- Are Final Market Prices Sufficient for Information Aggregation?: https://arxiv.org/abs/2509.14645
- Ornstein-Uhlenbeck Process for Horse Race Betting: https://arxiv.org/abs/2503.16470
