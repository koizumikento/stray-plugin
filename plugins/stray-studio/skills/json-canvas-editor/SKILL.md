---
name: "json-canvas-editor"
description: "Use when the user wants to create, edit, or repair a JSON Canvas 1.0 `.canvas` file with valid typed nodes, edges, IDs, and readable layout. Do not use for Mermaid, draw.io, generic whiteboards, ordinary JSON cleanup, or visual design work outside the JSON Canvas format."
---

# JSON Canvas Editor

Create and edit JSON Canvas files safely. Keep the focus on valid structure, stable IDs, readable layouts, and reference integrity.

Use this skill when working with `.canvas` files for mind maps, flowcharts, note graphs, or other JSON Canvas layouts.

## Do Not Use For

- draw.io, Mermaid, or other diagram formats
- broad visual design or presentation polish
- freeform brainstorming that does not need a valid `.canvas` file
- general JSON cleanup that is unrelated to JSON Canvas structure
- viewing or rendering an existing canvas when no structural change is requested

## Workflow

1. Confirm the canvas job and source file:
   - identify whether you are creating a new canvas or editing an existing one
   - read the target `.canvas` file before changing anything
   - if the user did not provide a file, ask for the path or the desired canvas content

2. Preserve the JSON Canvas shape:
   - keep a top-level object; JSON Canvas 1.0 permits `nodes` and `edges` to be omitted, but each must be an array when present
   - use the official JSON Canvas 1.0 specification as the field authority and avoid adding fields that are not needed for the requested canvas

3. Edit nodes carefully:
   - require every node to have a string `id` unique among nodes, a supported `type`, and integer `x`, `y`, `width`, and `height`
   - use only the standard node types `text`, `file`, `link`, and `group` unless the target application explicitly documents an extension
   - require `text` for `text` nodes, `file` for `file` nodes, and `url` for `link` nodes; keep group-only fields on `group` nodes
   - set `x`, `y`, `width`, and `height` so nodes do not overlap unless overlap is intentional
   - keep node text short enough to read inside the chosen size

4. Wire edges with valid references:
   - give every edge a string `id` unique among edges; prefer IDs that also avoid node-ID collisions for interoperability, but do not reject an otherwise valid file on that preference alone
   - require string `fromNode` and `toNode` values
   - connect only existing node IDs
   - do not leave dangling `fromNode` or `toNode` values
   - keep edge metadata minimal unless labels or styling are required

5. Lay out the graph for clarity:
   - space related nodes in rows, columns, or clusters
   - leave enough room for labels and edge routing
   - group connected nodes near each other instead of scattering them across the canvas

6. Validate before finishing:
   - parse the file as JSON
   - confirm `nodes` and `edges` are arrays when present and every object has its type-appropriate required fields
   - confirm node IDs are unique among nodes and edge IDs are unique among edges
   - confirm every `fromNode` and `toNode` resolves to a real node and no edge is dangling
   - confirm standard enum-like values such as node type, side, end shape, and group background style match JSON Canvas 1.0 when present
   - open the file in the intended canvas application when feasible; otherwise state that only structural validation was performed

## Output Expectations

- Return the edited `.canvas` content or the exact file path that was updated.
- Call out any validation issue that blocks saving the file.
- State which validation checks were run when the canvas was repaired or heavily changed.
- State whether validation covered JSON parsing, JSON Canvas 1.0 required fields, node/edge collection ID uniqueness, edge resolution, and an application-open check.
- If the canvas had to be simplified, say which nodes or edges were reduced or removed.

## Guardrails

- Do not rename IDs unless the change is necessary and the references are updated too.
- Do not convert the file into a general drawing format.
- Do not guess about missing nodes or edges when the source canvas is incomplete.
- Do not add styling noise when the job is about structure and correctness.
