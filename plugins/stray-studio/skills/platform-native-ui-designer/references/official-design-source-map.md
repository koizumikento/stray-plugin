# Design Source Map for Apple Platforms

Use this map to select the smallest official source set the user needs to open for a platform UI specification. Give the user the relevant links and ask them to write their own short notes about the relevant guidance, with provenance from pages they opened themselves. Do not ask for copied page text, images, or screenshots. The entries are routing links, not a copy of Apple guidance, and do not authorize automated retrieval.

## Source Priority

1. Ask the user to open the dated design update feed when the target OS, component, or technology may have changed.
2. Ask for a user-authored note about the exact Human Interface Guidelines topic that governs the material design decision.
3. Request user-authored notes about technology-specific design or developer documentation when a system feature has additional constraints.
4. Request Design Resources metadata only when the decision depends on current templates, symbols, fonts, tools, or production assets.
5. Use user-authored design video notes as supplemental explanation. Record the session year and do not treat inspiration or award pages as normative requirements.

## Official Entry Points

| Source | URL | Use |
| --- | --- | --- |
| Apple Design overview | <https://developer.apple.com/jp/design/> | Route into current guidelines, resources, tools, videos, and learning material. |
| Apple Design overview, English | <https://developer.apple.com/design/> | Start an English-language fallback without asserting an exact translated counterpart. |
| What's New in Design | <https://developer.apple.com/jp/design/whats-new/> | Check dated changes before making version-sensitive claims. The Japanese route may contain English content. |
| Design Pathway | <https://developer.apple.com/jp/design/get-started/> | Find the official learning path and the main HIG category routes. |
| Human Interface Guidelines | <https://developer.apple.com/jp/design/human-interface-guidelines/> | Start an exact-topic HIG lookup. The documentation experience requires JavaScript. |
| Human Interface Guidelines, English | <https://developer.apple.com/design/human-interface-guidelines/> | Start an English-language HIG fallback and let the user return the exact topic URL they reach. |
| Getting Started | <https://developer.apple.com/jp/design/human-interface-guidelines/getting-started> | Establish platform-level experience expectations. |
| Foundations | <https://developer.apple.com/jp/design/human-interface-guidelines/foundations> | Route visual, layout, typography, color, iconography, motion, and inclusion questions. |
| Patterns | <https://developer.apple.com/jp/design/human-interface-guidelines/patterns> | Route common tasks, flows, navigation, feedback, data entry, and system-experience questions. |
| Components | <https://developer.apple.com/jp/design/human-interface-guidelines/components> | Route controls, views, presentation, menus, bars, selection, and status questions. |
| Inputs | <https://developer.apple.com/jp/design/human-interface-guidelines/inputs> | Route touch, pointer, keyboard, controller, gaze, gesture, voice, and other input questions. |
| Technologies | <https://developer.apple.com/jp/design/human-interface-guidelines/technologies> | Route Apple service and system-feature design questions. |
| Apple Design Resources | <https://developer.apple.com/jp/design/resources/> | Verify current UI kits, templates, fonts, SF Symbols, Icon Composer, product bezels, and platform versions. Do not redistribute downloads. |
| Design Videos | <https://developer.apple.com/jp/videos/design/> | Find supporting WWDC and Tech Talks sessions. Record the year and prefer current guidance when sessions conflict. |
| Accessibility design guidance | <https://developer.apple.com/jp/design/human-interface-guidelines/accessibility> | Start accessibility design decisions with the platform-aware HIG topic. This documentation requires JavaScript. |
| Accessibility API documentation | <https://developer.apple.com/documentation/accessibility> | Use implementation-adjacent accessibility documentation when the HIG alone does not settle a requirement. This page is English and requires JavaScript. |

## Topic Routing

| Decision | Start with | Then narrow to |
| --- | --- | --- |
| First design for a platform | Getting Started | Relevant Foundations, Patterns, Components, and Inputs topics |
| Navigation or task flow | Patterns | Platform-specific component and input topics |
| Layout, typography, color, imagery, icons, or motion | Foundations | Exact topic plus Design Resources when an official asset or tool matters |
| Controls, menus, bars, lists, dialogs, search, or selection | Components | Exact component page and its platform coverage |
| Touch, pointer, keyboard, controller, gaze, hand, voice, or Digital Crown | Inputs | Exact input page and target-platform considerations |
| Widgets, Live Activities, Siri, App Shortcuts, Wallet, Apple Pay, SharePlay, or another system feature | Technologies | The feature's developer documentation and current design resources |
| New OS behavior, renamed guidance, or a changed component | What's New in Design | Exact HIG topic and its change information when available |
| UI kit, SF Symbols, font, Icon Composer, template, or product bezel | Apple Design Resources | The current download page and any asset-specific terms |
| Additional rationale or examples | Design Videos | A current session whose year and platform match the target |

## Language and Access Fallback

1. Give the user the Japanese official route first when it is likely to contain the relevant guidance.
2. If the user reports that the Japanese page is partial, English-only, or redirected, ask them to use the page's language switch or navigate from an English entry point above, then return the resulting exact URL with a short note in their own words. Do not assert an unverified one-to-one counterpart.
3. Preserve the page title, exact URL, visible language, visible publication or update date, and user-reported access date from the supplied source note.
4. HIG and some developer documentation require JavaScript. The user should open them in their normal browser; the agent must not use browser control, web retrieval, HTTP clients, or undocumented DocC internals to obtain the content.
5. If the user cannot supply a source note in their own words, mark the affected decision provisional instead of reconstructing current guidance from memory.

## Evidence Rules

- Accept a design claim only when the user provides their own note with an exact official URL and user-reported access date.
- Link the exact topic attributed by the user for each material platform-specific claim, and identify the claim as guidance reported in a user-supplied note.
- Record a publication or update date only when the user reports that it is visible on the page. Do not infer missing dates.
- Record source language and target platforms as user-reported, and do not extend a rule to an unlisted platform without labeling the extension as a recommendation.
- Treat What's New, resource versions, beta status, tool requirements, and download links as unstable. Do not call them current without a dated user-authored note, and describe freshness as user-reported.
- Treat older user-authored video notes as context, not proof of current platform behavior, unless newer user-supplied notes indicate that current documentation still points to them.
- Keep third-party sources outside this skill. Broader research may use another skill only for non-Apple sources; never use a handoff to retrieve or copy Apple-domain content.

## Boundaries and Related Official Sources

- App Store policy is a separate workflow: <https://developer.apple.com/jp/app-store/review/guidelines/>.
- Apple website content-use terms are published at <https://www.apple.com/jp/legal/internet-services/terms/site.html>.
- Apple copyright and trademark guidance is published at <https://www.apple.com/jp/legal/intellectual-property/guidelinesfor3rdparties.html>.
- Apple's current trademark list is published at <https://www.apple.com/legal/intellectual-property/trademark/appletmlist.html>.
- Do not access or retrieve content from Apple domains through browser control, web tools, search-result opening, HTTP clients, scripts, or undocumented data feeds.
- Do not invoke another skill, agent, connector, or tool to work around the Apple-domain retrieval or content-copy boundary.
- Do not crawl, mirror, bulk copy, or cache Apple content. Do not place Apple assets or downloadable design resources in this skill.
- Do not ask the user to copy, upload, or transmit Apple page text, images, screenshots, videos, or downloadable assets.
- Analyze only the user's own notes for the current task, paraphrase them, and do not present them as independently verified Apple wording.
- These operational boundaries are not legal advice. Escalate legal or licensing questions rather than interpreting permission.
