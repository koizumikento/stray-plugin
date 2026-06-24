# Android Reference

Use this reference when the primary user-facing surface is Android, when adding Android support to a cross-platform app, or when Android platform behavior materially affects the shipped flow.

## Stack Discovery

1. For existing Android projects, identify the current app shape before editing:
   - Kotlin or Java
   - Jetpack Compose, Views, or mixed UI
   - Android Studio, Gradle, Android Gradle Plugin, Kotlin, Compose compiler, and dependency management setup
   - navigation, state holder, lifecycle, dependency injection, persistence, networking, background work, permissions, deep links, notifications, testing, signing, and release pipeline
2. Preserve the repository's established Android conventions unless the user explicitly asks for a migration.
3. If the project already uses React Native, Expo, Flutter, Kotlin Multiplatform, Compose Multiplatform, Capacitor, or Trusted Web Activity, treat Android as one platform target inside that ecosystem and follow its Android integration guidance.

## New Android App Research Gate

Before scaffolding a new Android app, do a current ecosystem check. Avoid hardcoding volatile tool or library versions in the skill itself.

1. Check official Android Developers sources for:
   - Kotlin-first guidance
   - Jetpack Compose and AndroidX architecture recommendations
   - Android Studio, Gradle, Android Gradle Plugin, Kotlin, Compose compiler, and Compose BOM compatibility
   - Google Play target API, compile SDK, app bundle, signing, privacy, permissions, and policy-relevant release requirements
   - core app quality, adaptive app quality, performance, accessibility, and testing guidance
2. Limit new-app stack research to Kotlin/Compose and Flutter by default:
   - Native Android with Kotlin and Jetpack Compose for Android-first apps, deep platform integration, performance-sensitive flows, platform-native UX, or teams that can maintain native Android code
   - Flutter when Android and iOS parity, a consistent custom UI, single codebase delivery, or an existing Dart/Flutter team is a first-order requirement
3. Expand beyond Kotlin/Compose and Flutter only when the user explicitly asks, the repository already uses another mobile stack, or a hard product constraint makes the default candidates unsuitable.
4. Prefer current stable official releases for new work unless the user explicitly accepts preview, beta, or experimental APIs.
5. Record the sources and date used for any Android stack choice in the handoff when the choice materially affects maintenance.

## Native Android Defaults

- Treat Kotlin plus Jetpack Compose plus AndroidX architecture guidance as the native Android default when no stronger repository or product constraint exists.
- Keep UI state explicit and lifecycle-aware. Prefer ViewModels or established local state holders for screen state, and keep data access outside composables.
- Keep business data behind repositories or equivalent data-layer abstractions, even for small apps.
- Use version catalogs or the repository's existing dependency management pattern for Android dependencies.
- Use Hilt, WorkManager, DataStore, Room, Paging, Navigation, or other Jetpack libraries when they fit the flow, but verify current guidance and existing project conventions before adding them.
- Keep permissions lazy and explainable. Verify denial, revocation, and degraded behavior.
- Treat large screens, foldables, multi-window, keyboard, mouse, trackpad, and stylus behavior as part of Android quality when the app could reasonably run there.

## Implementation Checks

- Check Android lifecycle paths: cold start, warm start, process death where relevant, rotation or resizing, backgrounding, resume, interrupted flows, and deep links.
- For write or sync flows, verify pending, retry, duplicate-submit, offline, reconnect, stale cache, and read-after-write behavior.
- For background work, confirm whether the work must survive process death and use the platform-appropriate scheduler rather than a long-running foreground or background service by default.
- For platform integrations, check manifest declarations, runtime permissions, intent filters, notification channels, foreground service types, exported components, and privacy-sensitive logs.
- For Compose, verify recomposition-sensitive code, state hoisting, stable keys in lists, lifecycle-aware collection, accessibility semantics, previews where useful, and UI tests for critical behavior.

## Validation

Run the strongest feasible Android validation for the change:

- `./gradlew lint`
- targeted unit tests
- targeted instrumentation or Compose UI tests
- debug build or release build, depending on the affected path
- emulator or physical-device verification of the main user flow
- startup, scrolling, transition, ANR, crash, StrictMode, and permission-denial checks when relevant
- Google Play or release checks for target SDK, signing, app bundle, debug-only dependencies, sensitive data logging, and outdated dependencies when release behavior is touched

If emulator, device, signing, Play Console, or release validation is unavailable, state exactly what remains unverified.

## Guardrails

- Do not migrate Java to Kotlin, Views to Compose, fragments to single-activity Compose, or one cross-platform framework to another unless the task requires it.
- Do not add a new Android dependency just because it is popular; tie it to a user flow, platform requirement, or existing architecture pattern.
- Do not put network, disk, or database work directly in composables.
- Do not rely on client-only checks for authorization or paid/privileged feature access.
- Do not request broad permissions at startup unless the platform requirement and user flow justify it.
- Do not leave Android-specific behavior untested when permissions, background work, deep links, notifications, signing, or release settings changed.
