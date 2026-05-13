# Dynamic Visual Style Reference

Use this reference when an LP needs motion, layered product visuals, interactive hero treatments, animated proof, or conversion-supporting visual polish. The goal is to make the offer easier to understand and more credible, not to decorate the page or restyle an artifact independently from the landing-page message.

## Motion Roles

- Reveal: introduce product states, proof blocks, or section transitions as the visitor reaches them.
- Progress: show a workflow moving from input to output, draft to shipped, issue to resolved, or manual to automated.
- Compare: make before/after, old/new workflow, pricing/value, or feature differences legible.
- Focus: draw attention to the next CTA, active tab, live status, selected card, or changed product state.
- Confirm: respond to hover, press, submit, copy, filter, tab change, or successful form state.
- Ambient: use only when it reinforces the brand or product domain and does not compete with the message.

## Product Visual Treatments

- Real UI frame: use when screenshots or product surfaces are available. Keep labels, data, and states plausible enough to feel in use.
- Workflow stack: layer cards, messages, tickets, files, charts, or dashboards to show a process rather than a static screen.
- Output gallery: show finished artifacts, templates, generated results, customer examples, or before/after states.
- Core input surface: put the prompt box, search field, upload dropzone, code command, email capture, or booking form in the hero when that interaction is the product.
- System diagram: use for platforms, infrastructure, data flow, or integrations when screenshots would hide the value.
- Metric panel: pair quantified claims with compact charts, counters, uptime, savings, conversion, or scale numbers.

## Layout And Layering

- Establish stable dimensions for animated or layered regions with `min-height`, `aspect-ratio`, grid tracks, or explicit media containers.
- Keep text and CTAs outside moving layers unless the motion is very subtle and the text remains readable at all breakpoints.
- Use depth through spacing, shadows, borders, opacity, and overlap sparingly. One strong layered focal area beats many scattered floating elements.
- Anchor dynamic visuals to the section's message. The visitor should know why the visual exists without reading a caption.
- Reserve hero-scale motion for the hero or one flagship proof section. Keep secondary sections quieter.
- Make mobile layouts simpler: stack layers, reduce overlap, replace wide timelines with steps, and avoid tiny animated text.

## CSS And Interaction Patterns

- Use CSS transitions for hover, press, focus, tab, accordion, card lift, and subtle reveal states.
- Use keyframe animation for looping status, progress, marquee, pulse, shimmer, or background-position effects only when the loop has a clear purpose.
- Use intersection-triggered reveals for section entrance, but keep content present, readable, and visible by default. Apply reveal animation as progressive enhancement, not as the only path to visibility.
- Use scroll-linked effects only for high-value storytelling moments, and provide a static fallback.
- Use video when real product behavior matters and the file can be optimized, paused, captioned or transcribed when meaningful audio exists, and replaced with a poster image or static product proof.
- Use canvas, WebGL, or 3D only when the product domain or requested experience needs it. Follow the global frontend guidance for advanced rendering, including Three.js for 3D when applicable and screenshot plus canvas-pixel validation on desktop and mobile.
- Favor `transform` and `opacity` for motion. Avoid animating layout-triggering properties when possible.
- Limit infinite loops, shimmer, marquee, pulse, and background-position effects. Disable or simplify them for reduced motion, and pause decorative loops when offscreen when the stack supports it.

## Style System Guidance

- Define a small visual vocabulary before implementing: color roles, surface styles, border treatment, shadow depth, motion duration, easing, and media framing.
- Prefer a restrained palette with clear contrast. Avoid letting the page become one hue family unless the brand system already requires it.
- Match motion timing to intent: quick feedback for controls, moderate reveal for sections, slower motion only for ambient or narrative visuals.
- Keep easing consistent. Favor natural ease-out for entrances and short ease-in-out for state changes.
- Use iconography for tools, checks, arrows, statuses, and controls where it improves scanability.
- Let proof visuals carry detail; keep surrounding copy short and high-contrast.

## Accessibility And Performance

- Honor `prefers-reduced-motion` by disabling nonessential transforms, parallax, autoplay loops, and scroll-linked animation.
- Reduced-motion and no-JS states must not leave content hidden, offset, unclickable, or dependent on animation completion.
- Maintain keyboard focus visibility for interactive cards, tabs, accordions, buttons, and forms.
- Do not convey essential information only through motion, color, hover, or animation timing.
- Provide captions or transcripts for video with speech or meaningful audio, and visible controls or an equivalent pause mechanism for important media.
- Use muted, nonblocking autoplay only when it is decorative or has an equivalent accessible fallback.
- Avoid layout shift by reserving media dimensions before images, video, embeds, or generated visuals load.
- Optimize large images and video; use responsive sizes, lazy loading below the fold, and poster frames for video.
- Check that overlays, blur, glass effects, and gradients do not reduce text contrast.

## Dynamic Visual Checklist

- The hero has one clear visual proof strategy: product state, workflow, output, metric, system diagram, or core input.
- Motion supports a message: reveal, progress, compare, focus, confirm, or ambient.
- Every animated region has stable dimensions on desktop and mobile.
- Text, buttons, and forms remain readable and clickable while motion is running.
- Reveal content remains visible if JavaScript fails, animation does not run, or reduced motion is enabled.
- Reduced-motion behavior is defined for nonessential movement and does not leave elements hidden or displaced.
- Video with meaningful audio has captions/transcript support, controls or pause behavior, and a static fallback.
- Continuous animations avoid layout-triggering properties, are limited in number, and are reduced or paused when appropriate.
- The page still works when video, animation, or advanced rendering fails.
- Dynamic effects are consistent with the repository's existing stack and do not introduce heavy dependencies without a clear payoff.
