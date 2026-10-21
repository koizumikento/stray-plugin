# Editing Patterns

Use these patterns when syntax, figurative wording, contrast, or document conventions make an edit uncertain. Examples are local illustrations, not replacement rules. Apply the meaning checks in SKILL.md before adopting a change.

## Workflow

1. Identify the exact reading difficulty and the information the passage contributes.
2. Check the sentence and its context for the actor, action, object, modifier scope, and logical relationship. Distinguish an omitted but established detail from an unknown one.
3. Try the smallest change that resolves the difficulty. Prefer keeping a precise verb over replacing it with a broader or more abstract expression.
4. Compare meaning and tone, then read the paragraph again. Keep a natural original or an unresolved expression when the candidate would require guessing.

## Actors, Objects, and Scope

| Passage and context | Possible treatment | Reason |
|---|---|---|
| 「受付担当が申請を登録し、審査担当が承認します。」 | Keep it. | Two actors are explicit; repeating the subject serves a purpose. |
| 「申請が承認されると、自動的に通知します。」 Earlier text explicitly says the system sends the notice. | 「申請が承認されると、システムが自動的に通知します。」 | Names an established actor without assigning it the approval. |
| 「保存先と暗号化方式を確認しました。こちらは変更しません。」 No other context identifies 「こちら」. | Preserve the ambiguity and ask which setting is unchanged when commentary is allowed. | Proximity alone does not establish the referent. |
| 「担当者が確認した資料を送ります。」 | If the context establishes the intended reading, clarify it; otherwise retain it and ask. | It can mean that someone sends material checked by the contact, or that the contact sends already checked material. Do not assign both actions to the contact without evidence. |
| 「承認された申請だけを、翌朝まとめて送信します。」 | 「承認された申請だけを翌朝まとめて送信します。」 if the pause impedes reading. | A punctuation edit need not alter the actor, object, or approval condition. |
| 「圧縮して送信するため、添付ファイルは事前に選択してください。」 | Keep the purpose attached to the instruction when adjusting word order or punctuation. | Splitting it into unrelated statements can lose why the selection must happen first. |

Do not expand every omitted Japanese subject. A clearly continuing topic often reads better without repetition. If a technical component is the topic and a later clause mentions configuration or build steps, establish whether that clause describes the component's behavior or someone's setup action before adding an actor or location.

Preserve comparisons and quantifiers: 「全員が完了したわけではない」 does not mean 「誰も完了していない」. 「接続できれば取得する」 does not state that connecting is the only condition under which retrieval occurs.

## Metaphor and Technical Precision

| Passage | Possible treatment | Reason |
|---|---|---|
| 「この機能がチームの未来を切り拓きます。」 | Ask what benefit is intended if no concrete claim is supplied; retain the sentence if an edit would require inventing one. | Replacing it with a promise of faster work would add a claim. |
| 「確認作業に夕方の一時間を吸い取られました。」 | 「確認作業に夕方の一時間を費やしてしまいました。」 if the surrounding register fits. | Keeps duration and the writer's sense of an unwelcome cost. |
| 「ジョブは午前二時に起動し、処理結果を保存します。」 | Keep it. | A system subject describes actual behavior without implying human intent. |
| 「親プロセス」「デッドロック」「依存関係」 | Preserve established technical terms. | Figurative origins do not make a term an editing defect. |
| 「この区間は処理が重い。」 No measurements or cause are given. | Keep it or ask what observable behavior is meant if necessary for the reader. | Do not invent latency, CPU load, or a performance cause. |

Replacing a metaphor with a vague abstraction may leave the same problem. A plain verb must still preserve the original action: 「照合する」 is more specific than 「見る」, and 「保存しない」 does not say that an old value is deleted.

## Contrast, Emphasis, and Endings

1. Identify what a preface or contrast corrects, limits, or emphasizes. Remove it only if that contribution is absent in this context. For example, 「今回は画面の色ではなく、入力の順序を検証します」 distinguishes two test targets and should keep that distinction.
2. Preserve evaluations as evaluations. 「復旧手順の明確さが重要です」 cannot become 「復旧手順を明確にしてください」 without changing an assessment into a request.
3. Separate completion, current behavior, and plans. 「通知先を変更しました」, 「現在は運用担当に通知します」, and 「来週から通知先を増やします」 can coexist naturally in a change report.
4. Keep permission and commitment distinct. 「下書きを共有しても構いません」 permits sharing; it does not promise sharing capability. 「週末に停止する可能性があります」 is not a scheduled shutdown or a guarantee.
5. Vary sentence structure only when it improves reading without changing these functions. Repeated 「です」 or 「してください」 can be appropriate.

## Document Conventions

| Context | Preserve or adjust |
|---|---|
| Email and chat | Keep useful greetings, closing phrases, and courtesy. Adjust politeness only from explicit instructions or established context; do not invent apologies, gratitude, or relationships. |
| PR description and incident report | Keep distinct changes, verification results, and chronological events easy to scan. Do not turn untested behavior into a verified result or an unknown cause into a conclusion. |
| Procedure and meeting record | Keep numbered steps, decisions, owners, deadlines, and checklist structure. A label such as 「担当：佐藤」 conveys data directly. |
| Specification and formal document | Keep defined terms, conditions, permission, obligations, and guarantees precise, even when the wording is formal or long. |
| Research writing | Keep hedging, attribution, units, and causal limits. An association must not become a cause. |
| Personal or promotional writing | Preserve intentional rhythm, humor, emphasis, and fitting metaphor. Do not create lived experience, opinions, or product benefits. |

Treat length, punctuation, bold text, headings, and lists as tools for reading. Keep labels that identify values or named items. For a decorative label repeating its explanation, consider using the explanation alone only after checking for lost emphasis or meaning. Follow requested notation; otherwise avoid unrelated spelling, spacing, or style-guide normalization. Protect code, quotations, URLs, and literal interface labels from prose substitutions.
