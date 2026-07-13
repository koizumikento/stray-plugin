---
name: "platform-native-ui-designer"
description: "Use when a defined feature for iOS, iPadOS, macOS, watchOS, tvOS, or visionOS needs an implementation-ready UI spec grounded in user-authored notes from official Apple design pages, with source URLs and access dates. Do not use for strategy, UI audits, implementation, or Apple-page extraction."
---

# Platform-Native UI Designer

Turn a defined feature or flow for Apple platforms into an implementation-ready interface specification. Confirm the target platform and baseline, work from user-authored notes attributed to official pages they opened themselves, and separate guidance reported in those notes from product-specific design judgment.

## Do Not Use For

- Product discovery, feature strategy, positioning, or PRDs; use `product-designer`.
- Findings-first critique of an existing screen, screenshot, diff, or UI implementation; use `reviewer`.
- SwiftUI, UIKit, AppKit, RealityKit, application, or backend implementation; use `fullstack-app-builder` for current-repository app work or a more specialized available iOS or SwiftUI builder.
- Extracting, cleaning, or summarizing an Apple-domain URL. Do not hand Apple-domain retrieval to another skill; ask for user-authored notes or decline the extraction. Use `web-content-distiller` only for non-Apple URLs.
- Brand identity, marketing assets, app icons, screenshots, or visual theming as the primary deliverable.
- App Review Guidelines, legal advice, trademark clearance, or a guarantee of platform approval or accessibility conformance.

## Reference Loading

- Load `references/official-design-source-map.md` before requesting source material. It maps design decisions to official links the user can open and defines evidence, language, and content-use boundaries.
- Load `references/platform-design-checklist.md` before synthesis. Use only the sections relevant to the selected platform and flow.
- Use `references/validation-cases.md` when evaluating or changing this skill's routing behavior.

## Workflow

1. Confirm that the product decision is already defined.
   - State the feature, target user, primary task, intended outcome, and artifacts supplied by the user.
   - Identify what is settled and what remains a UI decision.
   - Route to `product-designer` when the user still needs to decide what to build or why.

2. Fix the Apple-platform context before designing.
   - Identify iOS, iPadOS, macOS, watchOS, tvOS, visionOS, or an explicit multi-platform set.
   - Record the supported OS baseline, device or window classes, orientation or resizing expectations, input methods, and relevant system integrations.
   - Record accessibility, localization, privacy, brand, technical, and delivery constraints that affect the interface.
   - Ask one short clarification when the primary task, target platform, or a materially version-sensitive OS baseline, device or window context, or input method cannot be inferred safely. Otherwise state a reasonable assumption and proceed, but never assume the latest OS version.

3. Request the smallest source-note packet.
   - Follow the source order and routing table in `references/official-design-source-map.md` to choose the smallest relevant category or entry-point links; do not claim to know the exact current topic page without user-supplied metadata.
   - Give the user those links and ask them to navigate in their normal browser to the exact topic pages relevant to the decision, then write a short note in their own words about the guidance they found.
   - Request the page title, exact URL, visible language, visible publication or update date, user-reported access date, and relevant platform coverage with each note.
   - Do not ask the user to copy, upload, or transmit Apple page text, images, screenshots, videos, or downloadable assets.
   - When the user already supplied sufficient source notes, use them without requesting the same notes again.
   - Do not access or retrieve Apple-domain content through browser control, web tools, search-result opening, HTTP clients, scripts, or undocumented data feeds.

4. Qualify the supplied source notes.
   - Confirm that each attributed source URL uses an official Apple domain and that the user's note identifies the relevant topic; do not claim independent verification of the page content.
   - Prefer notes from a complete Japanese page. When the user reports that it is partial, English-only, or redirected, ask them to use the page's language switch or navigate from an English entry point in `references/official-design-source-map.md`, then return the resulting exact URL with a new note in their own words.
   - Record dates and platform coverage as user-reported. Do not infer missing metadata.
   - Treat undated, incomplete, or version-mismatched notes as provisional and make the limitation visible before relying on them.

5. Translate the reported guidance into explicit interface decisions.
   - Define the information hierarchy, screen or scene map, navigation model, task flow, and important transitions.
   - Specify layout behavior, system or custom component roles, input behavior, feedback, and relevant platform integrations.
   - Cover loading, empty, success, validation, error, unavailable, permission, offline, interruption, and recovery states when they can occur.
   - Address accessibility, localization, content clarity, and alternate input paths as design requirements rather than optional polish.
   - Separate `Guidance reported in user-supplied notes`, `Design recommendation`, and `User or repository constraint`. Resolve multi-platform differences explicitly instead of generalizing from one platform.

6. Produce an implementation-ready specification.
   - Use the output shape in `references/platform-design-checklist.md`.
   - Make each important decision concrete enough for a designer or engineer to implement without choosing the interaction model again.
   - Include variants and responsive or adaptive behavior where device, window, orientation, content size, or input changes the experience.
   - Avoid unsupported pixel values, fabricated platform rules, and decorative imitation of Apple surfaces.

7. Validate the specification.
   - Confirm that every material platform-specific claim links to the exact official topic attributed in the user's source notes rather than only the design homepage.
   - Confirm the platform, OS baseline, device or window context, and input methods are visible in the deliverable.
   - Check the relevant items in `references/platform-design-checklist.md`, including accessibility and non-happy-path states.
   - Confirm that recommendations are labeled as recommendations and do not claim Apple endorsement, App Store approval, or complete compliance.

8. Handle evidence gaps without retrieving the source automatically.
   - Provide the Japanese category or entry-point link. When an English fallback is needed, point to an English entry point in `references/official-design-source-map.md` and ask the user to return the exact topic URL they reached; do not assert an unverified counterpart.
   - If the user cannot supply a note in their own words, state the gap and mark the affected decision provisional.
   - Do not reconstruct current guidance from memory or repeatedly ask for evidence that is not essential to the requested specification.

9. Hand off without absorbing implementation or review work.
   - If implementation is also requested, finish the UI specification and pass it to `fullstack-app-builder` for current-repository app work or to a more specialized available iOS or SwiftUI builder.
   - If the user wants findings-first evaluation of an existing UI, pass the artifact and source ledger to `reviewer`.
   - Do not claim that code, assets, prototypes, simulator checks, or App Store checks were completed by this skill.

## Output

- Scope, target platform, OS baseline, device or window context, input methods, and assumptions
- User-supplied source-note ledger with attributed official links, user-reported language and dates, and access date
- Screen, scene, or flow structure with state coverage
- Platform-specific navigation, layout, component, input, feedback, and system-integration decisions
- Explicit separation of guidance reported in user-supplied notes, design recommendations, and user or repository constraints
- Accessibility, localization, adaptation, and recovery requirements
- Acceptance checklist and implementation handoff notes

## Guardrails

- Treat this as an independent, unofficial workflow; never imply Apple authorship, sponsorship, endorsement, or approval.
- Do not access or retrieve content from Apple domains through browser control, web tools, search-result opening, HTTP clients, scripts, or undocumented data feeds.
- Do not invoke another skill, agent, connector, or tool to work around the Apple-domain retrieval or content-copy boundary.
- Do not mirror, bulk extract, translate, or redistribute Apple pages, videos, images, fonts, UI kits, templates, product bezels, or other downloadable assets.
- Do not add crawlers, page-scraping scripts, DocC-internal data collectors, or a cached HIG corpus.
- Do not ask the user to copy or transmit Apple page content. Work only from their own notes and the accompanying source metadata.
- Paraphrase user-supplied notes and link their attributed source; do not present the notes as independently verified Apple wording. Escalate when exact wording materially affects a decision.
- Never hardcode or claim the latest OS, HIG state, tool version, or asset version without dated user-supplied notes, and describe freshness as user-reported.
- Stop and disclose the evidence gap when the user cannot supply a current source note and the design decision depends on it.
