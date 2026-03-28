---
name: "json-canvas-editor"
description: "Use when the user wants to create, edit, or repair JSON Canvas `.canvas` files, including node layout, edge wiring, IDs, and structural validation. Do not use for generic diagramming, draw.io, whiteboard sketches, or visual design work."
---

# JSON Canvas Editor

Create and edit JSON Canvas files safely. Keep the focus on valid structure, stable IDs, readable layouts, and reference integrity.

Use this skill when working with `.canvas` files for mind maps, flowcharts, note graphs, or other JSON Canvas layouts.

## Do Not Use For

- draw.io, Mermaid, or other diagram formats
- broad visual design or presentation polish
- freeform brainstorming that does not need a valid `.canvas` file
- general JSON cleanup that is unrelated to JSON Canvas structure

## Workflow

1. Confirm the canvas job and source file:
   - identify whether you are creating a new canvas or editing an existing one
   - read the target `.canvas` file before changing anything
   - if the user did not provide a file, ask for the path or the desired canvas content

2. Preserve the JSON Canvas shape:
   - keep a top-level object with `nodes` and `edges`
   - keep node and edge objects valid JSON
   - avoid adding fields that are not needed for the requested canvas

3. Edit nodes carefully:
   - give every node a unique ID
   - keep node `type` values consistent with the content
   - set `x`, `y`, `width`, and `height` so nodes do not overlap unless overlap is intentional
   - keep node text short enough to read inside the chosen size

4. Wire edges with valid references:
   - connect only existing node IDs
   - do not leave dangling `fromNode` or `toNode` values
   - keep edge metadata minimal unless labels or styling are required

5. Lay out the graph for clarity:
   - space related nodes in rows, columns, or clusters
   - leave enough room for labels and edge routing
   - group connected nodes near each other instead of scattering them across the canvas

6. Validate before finishing:
   - parse the file as JSON
   - confirm all node IDs are unique
   - confirm every edge target resolves to a real node
   - verify the file still matches JSON Canvas expectations after the edit

## Output Expectations

- Return the edited `.canvas` content or the exact file path that was updated.
- Call out any validation issue that blocks saving the file.
- State which validation checks were run when the canvas was repaired or heavily changed.
- If the canvas had to be simplified, say which nodes or edges were reduced or removed.

## Guardrails

- Do not rename IDs unless the change is necessary and the references are updated too.
- Do not convert the file into a general drawing format.
- Do not guess about missing nodes or edges when the source canvas is incomplete.
- Do not add styling noise when the job is about structure and correctness.
