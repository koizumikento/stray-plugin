# ChatGPT MCP App Extensions Reference

Read this when implementing or debugging a ChatGPT MCP App's sidebar or conversation entrypoint, file viewer/editor, settings, display mode, deep link, model context, composer mentions, or rich forms. Keep the app flow here; route standalone MCP contract design or review to `mcp-server-designer`.

## Sources And Compatibility

Checked on 2026-10-01 against the [OpenAI overview](https://developers.openai.com/plugins/build/extensions), [formal specification](https://github.com/openai/mcp-extensions/blob/900032d8bd7c1566202d0cb1666986584f932043/docs/spec.md), [TypeScript SDK guide](https://github.com/openai/mcp-extensions/blob/900032d8bd7c1566202d0cb1666986584f932043/typescript/README.md), and [Python SDK guide](https://github.com/openai/mcp-extensions/blob/900032d8bd7c1566202d0cb1666986584f932043/python/README.md). These extend MCP and MCP Apps; they are not a replacement protocol or a requirement for ordinary app work.

1. Identify the target ChatGPT product, platform, client version when available, connection type, MCP revision, installed SDK versions, and existing server/UI registration before editing. Recheck the current overview and corresponding sections of the [latest specification](https://github.com/openai/mcp-extensions/blob/main/docs/spec.md) for the requested feature.
2. Treat availability as a compatibility check. The overview announces future web availability for Free/Go and desktop-only composer mentions. The specification's support table describes expected launch support, and its Web column refers to the Work browser, excluding classic ChatGPT. Do not present that table as observed support for every account or client.
3. Reuse the project's MCP and MCP Apps stack. TypeScript uses `@openai/mcp-extensions/server` on the server and `@openai/mcp-extensions/app` in the UI. Python's `openai-mcp-extensions` is server-side; the app still uses the TypeScript app SDK. Confirm compatible dependencies and public API names instead of pasting setup from a different SDK generation.
4. Check negotiated capabilities after initialization. App extension fields such as `resources`, `modelContext`, and `message` may be undefined before connection or remain unavailable on an unsupported host. Render a usable fallback where the requested flow permits one; otherwise report the unsupported requirement. Do not silently report a skipped save or context update as successful.

## Registration And First Render

1. Register the HTML UI resource with the MCP Apps resource MIME type, then associate it with the app tool through `_meta.ui.resourceUri`. Add entrypoints under the tool's `_meta["openai/ui"]`; place display-mode metadata on the UI resource's returned content item.
2. Accept empty arguments for `global` and `thread` entrypoints. Give each thread view a useful title distinct from the plugin name and provide an appropriate tool icon. A thread entrypoint has a separate instance in each conversation; scope its state accordingly.
3. Register initial tool-input and tool-result handlers before `app.connect()`. Render the supplied initial result rather than calling the tool again. Apply host theme/style variables at connection and on `hostcontextchanged`; bundle required CSS within the UI resource when external stylesheets are blocked by CSP.

Minimal tool metadata, after registering `ui://parts/viewer`:

```ts
import type { OpenAIUiToolMetadata } from "@openai/mcp-extensions/server";

const toolMetadata = {
  ui: { resourceUri: "ui://parts/viewer" },
  "openai/ui": {
    entrypoints: [{ type: "file", extensions: [".stl"] }],
  } satisfies OpenAIUiToolMetadata,
};
```

Use `{ type: "global" }` for sidebar launch or `{ type: "thread" }` for a conversation panel. File extensions must start with a dot, as required by the formal specification. Entrypoint invocation ignores `_meta.ui.visibility`; visibility is not an authorization control.

## Feature Contracts

| Feature | Implementation checks |
|---|---|
| Sidebar and conversation panels | Keep entrypoint opening safe with `{}` and use the initial result. Global desktop apps have an associated thread; context and messages target that thread. Do not mix state between conversations or app instances. |
| Display modes | Declare `availableDisplayModes` and optional `preferredDisplayMode` in resource `_meta["openai/ui"]`, consistent with the app's advertised modes. The checked specification supports `inline` and `fullscreen`, not `pip`; static entrypoints use `fullscreen`. Treat the preference as a hint and adapt to the actual host display mode. |
| Deep links | Handle `hostContext["openai/deepLink"]` on initialization and subsequent host-context changes. Percent-encode the plugin ID, tool name as one segment, and complete app-relative URL as the `path` query value. The decoded route must begin with `/` and contain no fragment. Validate the route and enforce access to the selected record. Use the specification's platform-specific link format. |
| Settings | Distinguish native structured settings from a bespoke app opened by a settings action. Keep the read tool read-only, accept `{}`, declare its output schema, and provide a value for every property. Updates contain changed properties only; merge them with persisted settings under the authenticated account and return the resulting values. |
| Model context | `ui/update-model-context` replaces the context supplied by the same app instance. Restore host-provided context on initialization/remount and react to attachment removal through host-context changes. Send only needed data. Content-block `_meta` is excluded from model input, but `annotations.audience: ["assistant"]` hides a block from the user while still sending it to the model. Never use that annotation to protect confidential data. |
| Messages | Distinguish context updates from sending a user message. The checked `ui/message` extension defaults to `{ target: "active", send: true }`; mobile supports only that behavior. Require an authorized user action for sending and preserve the current composer draft. Do not assume the app receives notifications for removal of message items from the composer. |
| Composer mentions | Register a mention-search handler/tool and include `app` in its UI visibility. Validate the query and filter results by the caller's permissions before returning resource links, titles, or previews. Verify the desktop picker rather than treating tool registration as UI proof. |
| Rich forms | Check host support for the complete schema; unsupported input types reject the form rather than yielding a partial UI. OpenAI-registered servers require MCP `2026-07-28` or later with multi-round-trip requests (MRTR). SDK `elicitInput`/`elicit_input` examples use the legacy direct-connection flow and do not implement MRTR. Validate submitted values and handle accept, decline, and cancel before applying effects. |

For rich forms, use titled `const` options with optional descriptions and `x-openai-thumbnail`; thumbnail sources must be HTTPS or image data URIs. Use `x-openai-suggestions` only when free-form values are allowed. For resource pickers use `x-openai-input.type: "resource"`, not the deprecated `"file"` alias. Check URI selection, defaults, multi-select mode, and upload support against the current specification; web forms requested through MCP Apps support explicit resource selection without uploads.

## File Reading And Saving

1. Parse the file tool input with the SDK schema, such as `OpenAIFileEntrypointInputSchema`, before using `file.resourceUri`. Treat that URI as opaque, not as a filesystem path or a remote download URL. Host-intercepted resource APIs read the opened file; choose `text` or `blob` representation when necessary and handle both if unspecified.
2. Subscribe to resource changes only while viewing the file. Remove update handlers and unsubscribe when changing files or closing the view. Keep external updates from erasing unsaved edits; apply [client-state guidance](client-state.md) for draft ownership and delayed responses.
3. Enable saving only when read metadata says `writable: true` and the negotiated write API exists. Write only to the URI supplied for the file entrypoint. Pass the observed ETag as `ifMatch` when available; if no ETag exists, acknowledge that the host cannot provide that version check and choose behavior consistent with the app's conflict policy.
4. Handle `saved`, `conflict`, and `too-large` results explicitly. A conflict or size rejection is not a save. Preserve the draft, show the reason, and reconcile/reload without automatically overwriting the newer file. Confirm the resulting contents when verifying the save path.
5. For server-side access to related files, use the SDK's `getResourcePath`/`get_resource_path` to read host-added `_meta["openai/resource"]["path"]`. Restrict operations to the authorized directory, validate paths before access, and reject traversal or symlink escapes. Do not expose raw host paths or file contents to the UI/model merely because a server can access them.

Use [identity/access guidance](identity-access.md) for settings, search, record access, and account transitions; [API guidance](api-communication.md) for uncertain write outcomes and retries. Host capabilities, UI visibility, and file type matching do not replace authorization.

## Validation And Handoff

1. Run existing targeted type/schema/build checks for the selected SDK and metadata. Validate registered resources, dot-prefixed extensions, empty entrypoint input, handlers installed before connection, and unsupported-capability behavior using the smallest applicable local harness.
2. Exercise the implemented feature's relevant paths: initial result and remount, separate conversations/accounts, deep links and forbidden records, settings read/partial update, context removal, authorized message sending, mention search, and form accept/decline/cancel or unsupported schema. For editors include external file changes, read-only access, save success, conflict, size rejection, and preserved drafts.
3. When the authorized target client is available, inspect the actual entrypoint, panel, editor, picker, or form and follow the [connect-and-test guide](https://developers.openai.com/plugins/deploy/connect-chatgpt). Record the tested client/platform and feature. Schema validation, mocks, and compilation are distinct from live host UI evidence.
4. Report implemented features, dependency/protocol assumptions, checks run, unsupported platforms, and host behaviors not observed. If the target client, credentials, or a required capability is unavailable, complete local work and identify the unmet check. Do not install a plugin, register a live connection, send messages, publish, or deploy unless existing authorization covers that target and effect.
