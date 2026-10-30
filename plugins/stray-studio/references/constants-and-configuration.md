# Constants And Configuration

Use this reference before introducing or changing meaningful fixed values, configuration sources, defaults, or overrides. For reviews, inspect the affected decisions without expanding the review scope or authorizing edits. Apply only relevant sections; an obvious local literal needs no inventory or design document.

## Workflow

1. Inspect existing constants, settings loaders, schemas, deployment inputs, and actual consumers before adding another source. Classify values by meaning, owner, scope, and when they must change. The same numeric value does not establish shared meaning.

   | Kind | Examples | Owner and placement |
   |---|---|---|
   | Code-owned invariant or fixed vocabulary | Unit conversions, protocol values, fixed business rules, status identifiers | Owning module's named constant, type, enum, or existing SDK definition; version with behavior |
   | Deployment setting | Service endpoint, region, resource identifier | Existing deployment inputs and runtime configuration boundary; keep deployment-specific values out of application logic |
   | Operational tuning | Timeouts, retry budgets, batch sizes, model selection | Existing settings mechanism when operators actually need adjustment; otherwise an intentional named code default near its owner |
   | User or tenant setting | Notification preference, organization-specific limit | Existing persistent settings owner, with access control and explicit user/tenant scope |
   | Secret | API key, password, signing key | Existing secret-management and runtime identity mechanism; expose only to authorized consumers |
   | Content or presentation value | Contact details, CTA targets, translated text, design tokens | Existing content/data module, localization catalog, or design system when applicable; do not turn ordinary copy into environment variables |
   | Self-explanatory local literal | Empty collections, simple counters, local array indices | Keep inline when the context fully explains it |

2. Choose the smallest appropriate representation and location before writing.
   - Name a value when its business or operational meaning, unit, reuse, or independent reason to change would otherwise be hidden. Prefer names such as `requestTimeoutMs` over `timeout` or `magicNumber`.
   - Keep a private constant near its owner. Share only when consumers need the same meaning and change together; equal values for unrelated purposes must remain independent. Reuse framework/SDK definitions instead of copying protocol values.
   - Preserve framework-required configuration paths and existing responsibility boundaries. Avoid a catch-all `constants`/`config` module, parallel settings loaders, or a new dependency when existing mechanisms suffice. Follow [source layout](source-layout.md) for new or moved files.
   - Externalize values that must vary independently of a code release. Do not create switches, environment variables, remote configuration, or a settings service for hypothetical flexibility. A safe, deliberate default or provider default may remain when its meaning and applicability are established.
3. Resolve configuration at the existing boundary and give consumers the settings they need.
   - Keep source lookup, parsing, validation, and defaults authoritative in one mechanism; do not scatter environment reads and fallback literals through handlers, components, and jobs. Use framework-native access or existing dependency injection rather than building a wrapper solely for uniformity.
   - Define relevant types, units, valid ranges, required/optional conditions, and cross-field constraints. Parse booleans explicitly; distinguish missing, empty, malformed, and valid zero/false values according to the contract.
   - Preserve the framework/repository's actual source precedence, including CLI overrides, environment variables, files, persistent settings, and defaults. Document non-obvious overrides; do not invent a universal precedence or duplicate defaults in callers and deployment templates.
   - Validate application-wide required settings before serving work. Validate optional-feature or tenant settings at their activation/use boundary so unrelated features do not require unused credentials. Reject invalid supplied values rather than silently replacing them with defaults. Never fall back from missing production credentials or targets to development ones.
   - Permit explicit test inputs through the existing configuration path. Avoid mutable global settings or import-time environment capture that makes tests order-dependent; account for framework initialization and build-time execution.
4. Define visibility and change lifecycle.
   - Distinguish build-time, process-start, per-request/tenant, and dynamically refreshed settings. State whether changes need a rebuild, restart/redeploy, or a supported refresh. Do not promise hot reload or add polling without a requirement.
   - Treat values shipped to a browser, mobile binary, desktop package, or public runtime-config response as public. Export only the approved public subset; never serialize the entire settings object or rely on an environment-variable prefix to protect secrets.
   - Use existing workload identity and secret storage/injection. Environment variables are a delivery mechanism, not a secret store. Follow the target platform's supported approach; do not mandate a new secret API, mounted file, or toolchain for every app.
   - Keep secret values out of source, tracked examples, build arguments/artifacts, logs, exception details, and configuration dumps. Use synthetic placeholders in examples. Preserve least privilege, rotation behavior, and the applicable [IaC credential lifecycle](iac-baseline.md) when infrastructure is affected.
5. Carry the changed contract through its actual consumers.
   - Align affected application code, schemas, deployment/IaC inputs, CI settings, environment examples, tests, and existing setup/operations documentation. Update only the relevant consumers; do not introduce a second source of truth or a new report file.
   - For renamed/removed settings, inspect callers and deployed inputs before choosing compatibility or rollout sequencing. Preserve authorization boundaries; editing a template does not establish that hosted configuration changed.
6. Validate the affected behavior and hand off its limits.
   - Use the smallest relevant checks for default selection, supplied overrides, missing required values, invalid/empty inputs, units/ranges, and source precedence. Cover optional-feature activation, user/tenant isolation, public exposure, and reload/restart behavior when affected.
   - Verify consumers use the resolved setting and do not retain an independent literal or fallback. Check examples and deployment wiring without displaying real secrets. A schema test alone does not prove the deployed value, client bundle, or runtime behavior.
   - Apply only useful existing lint rules. A numeric-literal ban cannot determine ownership or configuration lifecycle; do not rewrite every `0`/`1`, copy string literals into constants mechanically, or make tests import the same constant as their sole expected-value oracle.
   - Report new/changed keys, required/default behavior, public/server scope, and rebuild/restart/migration requirements when material. Distinguish structural checks from actual runtime or model evaluation evidence.

## Validation Cases

These synthetic cases are a decision rubric, not evidence that an agent executed the guidance correctly.

| Case | Expected decision | Failure |
|---|---|---|
| API endpoint differs between staging and production | Resolve the endpoint through existing deployment configuration | Move the production URL from a handler to a committed constant |
| Private unit conversion is used in one module | Name locally when it clarifies meaning | Add an environment variable or global constants bucket |
| Transport timeout and UI dismissal delay both equal `5000` | Keep separate meanings and explicit units | Share one constant solely because the numbers match |
| Timeout is an operator-adjustable setting | Resolve, parse, validate, and default through the existing settings boundary | Repeat environment reads and different fallbacks in each caller |
| Supplied timeout is empty, negative, or malformed | Apply the documented contract and reject invalid input | Silently use the default and hide the deployment error |
| A boolean override is `false` or a valid numeric override is `0` | Preserve it when allowed by the setting contract | Truthiness fallback replaces a valid explicit value |
| Optional integration is disabled and has no API key | Keep unrelated flows usable; validate before enabling/using the integration | Require every integration's secrets at global startup |
| Organization-specific limit can change in the product | Use the existing authorized tenant settings path | Use one process-wide environment variable for all tenants |
| Public frontend configuration is frozen by the bundler | State build timing and rebuild needs, or use an existing public runtime path | Promise an environment change updates an already-built client |
| Secret is available to the server | Keep it out of public subsets, error details, and build artifacts | Return the full settings object to the client |
| Corporate contact details or shared brand colors need reuse | Use existing site data or design tokens | Add environment variables for every text/style literal |
| IaC has an intentional supported provider default | Preserve it unless requirements require an explicit value | Parameterize or pin every provider setting without a reason |

## Sources And Applicability

Evidence checked: 2026-10-30. The workflow and cases are engineering guidance synthesized from these sources, not a universal framework contract or measured improvement in agent behavior. Verify the target framework/provider version when its loading, visibility, or refresh semantics matter.

- [Twelve-Factor: Config](https://12factor.net/config): deployment-varying configuration is separate from code; internal application wiring can remain in code. Its environment-variable recommendation does not make environment variables a secret store.
- [Fowler: Replace Magic Literal](https://refactoring.com/catalog/replaceMagicLiteral.html): use a meaningful named constant to expose a literal's meaning.
- [Microsoft: Options pattern](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/configuration/options?view=aspnetcore-10.0): related typed settings, consumer separation, validation, and explicit startup validation. Use the equivalent existing mechanism in other stacks.
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/): typed settings, defaults, source priority, and test overrides; do not assume its precedence applies to other loaders.
- [Next.js: Environment variables](https://nextjs.org/docs/app/guides/environment-variables): public-prefixed values are bundled at build time; changing the runtime environment does not update them.
- [Google Cloud: Secret Manager best practices](https://docs.cloud.google.com/secret-manager/docs/best-practices): least privilege, workload identity, leakage risks, and product-dependent secret delivery.
- [ESLint: no-magic-numbers](https://eslint.org/docs/latest/rules/no-magic-numbers): a supplementary numeric-literal rule with configurable exceptions, not a configuration-design check.
