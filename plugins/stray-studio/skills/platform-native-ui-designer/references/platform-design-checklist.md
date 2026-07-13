# Platform Design Checklist

Use only the sections that materially affect the selected feature and platform. Turn each applicable question into a concrete design decision or an explicit non-applicable note, and cite the exact official URL attributed in the user's source note for each material platform claim.

## 1. Context Header

- Target platform or platform set
- Supported OS baseline; current or beta status when relevant
- Device, display, orientation, window, scene, or spatial context
- Primary and alternate input methods
- Primary user, task, success condition, and frequency of use
- Repository, product, brand, privacy, localization, accessibility, and delivery constraints
- Supplied artifacts and unresolved assumptions

## 2. Information Architecture and Flow

- What is the user's primary task, and what is the shortest understandable path to completion?
- Which information and actions are primary, secondary, contextual, destructive, or reversible?
- What navigation model fits the platform and content depth?
- What is preserved when the user navigates away, changes window size, switches device context, or returns later?
- What explicit escape, cancel, undo, back, close, or recovery path exists?

## 3. Layout and Adaptation

- How does the hierarchy survive compact, expanded, resized, rotated, split, zoomed, or spatial presentation?
- Which regions are fixed, flexible, scrollable, persistent, collapsible, or conditional?
- How do safe areas, system chrome, keyboards, pointers, focus, and accessibility text sizes affect placement?
- What happens with short, long, missing, localized, right-to-left, or user-generated content?
- Which behaviors are shared across platforms, and which require a platform-specific variant?

## 4. Components and System Integration

- Which system components communicate the intended behavior without relearning?
- Where is a custom component truly necessary, and how will it preserve expected semantics and input behavior?
- Which capabilities belong in menus, toolbars, sidebars, tabs, inspectors, sheets, alerts, context menus, commands, widgets, complications, or spatial scenes?
- Which system technologies or services materially improve the task?
- Are official symbols, fonts, templates, or tools relevant, and has the user supplied a dated note identifying the version they saw rather than copying the asset into the project blindly?

## 5. Interaction, Input, and Feedback

- What is the primary action for each state, and is it reachable through every supported input method?
- What are the focus, hover, selection, pressed, disabled, loading, and completion behaviors?
- What keyboard shortcuts, pointer actions, controller focus moves, gaze or hand actions, Digital Crown behavior, voice alternatives, or touch gestures are required?
- What visible, audible, haptic, or spatial feedback confirms progress and results without unnecessary interruption?
- Are gestures or hidden interactions backed by a discoverable alternative?

## 6. State and Recovery Coverage

- Initial, loading, empty, populated, partial, success, validation, error, unavailable, permission-denied, offline, interrupted, and restored states
- First use versus returning use
- Zero, one, and many items where collection size changes the UI
- Stale, conflicting, or externally changed data
- Duplicate submission, cancellation, retry, undo, and destructive confirmation
- Backgrounding, relaunch, window restoration, and cross-device continuation when relevant

## 7. Accessibility and Inclusion

- Semantic names, roles, values, grouping, and reading or focus order
- Dynamic text or equivalent scaling without clipping, overlap, or loss of action
- Sufficient differentiation without relying only on color, motion, sound, depth, or position
- Alternatives for motion, haptics, audio, gesture, gaze, pointer, keyboard, controller, and touch where applicable
- Reachability and target clarity for the device and input context
- Captions, transcripts, descriptions, and controls for time-based media when relevant
- Content that remains understandable across literacy, language, and cognitive load differences

## 8. Platform-Specific Prompts

### iOS

- Touch-first reachability, transient interruptions, keyboard appearance, safe areas, orientation, and compact presentation
- Clear navigation and recovery when the user moves between app and system surfaces

### iPadOS

- Window resizing and multitasking, pointer and keyboard use, sidebars or inspectors, drag and drop, and external displays
- A layout that earns the larger canvas instead of stretching the iPhone hierarchy

### macOS

- Multiple windows, menu bar commands, toolbars, sidebars or inspectors, keyboard shortcuts, pointer precision, context menus, and window restoration
- Clear placement of document, app-wide, selection-specific, and destructive actions

### watchOS

- Brief, glanceable tasks, small-display hierarchy, Digital Crown or touch input, complications or Smart Stack relevance, and interruption cost
- A flow that avoids importing a full iPhone information architecture

### tvOS

- Focus movement, remote or controller input, viewing distance, overscan-safe composition, playback context, and clear selection state
- Interaction paths that do not depend on touch or pointer conventions

### visionOS

- Window, volume, or immersive-space choice; gaze and hand input; target comfort; depth; motion; surroundings; and transitions between immersion levels
- Essential controls that remain discoverable and usable without excessive reach, head movement, visual clutter, or forced immersion

## 9. Source and Decision Integrity

- Every material platform claim links to the exact official URL attributed in the user's source note.
- Guidance reported in user-supplied notes, product-specific recommendation, and user or repository constraint are labeled separately.
- Source language, dates, platform coverage, OS versions, and asset versions are identified as user-reported rather than independently verified or permanently current.
- A shared multi-platform rule is used only when the supplied notes and interaction model genuinely support it.
- Deviations from guidance include the user benefit, tradeoff, and validation needed.
- The specification does not imply Apple endorsement, App Store approval, or complete accessibility conformance.

## Output Shape

```markdown
# <Feature> — UI Specification for Apple Platforms

## Scope and assumptions
- Platform / OS baseline / device or window / input
- Primary task and success condition
- Constraints and supplied artifacts

## User-supplied source-note ledger
| User-reported page title | Attributed official URL | User-reported language | User-reported platform relevance | User-reported published or updated date | User-reported access date | Applied to |

## Experience structure
- Screen, scene, window, or flow map
- Navigation and transition model

## State model
| State | User sees | Available actions | Feedback and recovery |

## Interface decisions
### Guidance reported in user-supplied notes
### Design recommendations
### User or repository constraints

## Adaptation and accessibility
- Device, window, orientation, content-size, localization, and alternate-input behavior

## Acceptance checklist
- Observable conditions an implementation or prototype must satisfy

## Handoff notes
- Decisions fixed by this specification
- Provisional decisions and missing evidence
- Implementation, prototype, asset, or review work still required
```
