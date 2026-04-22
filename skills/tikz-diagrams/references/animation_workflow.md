# Animation Workflow

Use this reference for TikZ/PGF animations, `animate.sty` PDFs, animated teaching figures, and animation stress tests.

## Animation Design Gate

Before writing code, answer:

- What changes over time?
- Why is animation better than a static figure?
- How long does the viewer need to absorb each change, and which states need holds?
- What source pattern or existing component is being adapted?
- What is the minimum set of moving elements needed?
- Which frames are edge cases: first, middle, final, zero-overlap, threshold crossing, or peak risk?
- Should the change be discrete, continuous, or mixed?

Good animation jobs include:

- area accumulation, such as surplus, integrals, exposure, losses, or coverage
- parameter sweeps, such as EOQ, sensitivity, elasticities, or risk tolerance
- overlap and convolution, such as independent shocks, matching, or shared support
- discrete state transfer, such as cohorts, queues, inventory states, or workflow stages
- trajectory against a reference, such as margin buffers, target paths, or forecast bands
- recursive or iterative processes, such as sorting, allocation, convergence, or learning

Avoid animation when the only change is decorative motion, when a static small multiple would be clearer, or when the prompt asks for several unrelated ideas at once.

## Motion Form Gate

Choose the motion form before choosing frame count.

- Use **discrete build** when the viewer must notice a sequence of categorical additions: nodes in a game tree, steps in a proof, compliance types, workflow stages, or a before/after diagnostic.
- Use **continuous sweep/fill** when the concept is accumulation, progress along a curve, phase traversal, distribution-parameter change, threshold approach, or a moving state in a continuous geometry.
- Use **mixed motion** when the geometry changes continuously but interpretation changes at named regimes. Keep the continuous object smooth, but hold or switch labels only at meaningful boundaries.
- Prefer more intermediate frames over larger jumps when the viewer is meant to perceive direction, speed, curvature, accumulation, or path dependence.
- Avoid smooth motion for fundamentally categorical changes; it can imply continuity that is not part of the model.
- For circular fills, avoid drawing a nearly full 360-degree TikZ arc in one command. Draw completed segments plus one short current segment, as in `templates/animation_smooth_cycle_fill.tex`.

## Smoothness Cost Gate

Ask the user before rendering smooth transitions when the smoother version will materially increase render time or artifact size and the user has not already requested smooth animation.

Ask first when any of these are true:

- The smooth version needs more than about 60 frames, more than one heavy frame deck, or several high-DPI previews.
- The figure contains expensive content such as dense plots, image inclusions, many text boxes, transparency-heavy layers, or repeated external computations.
- The task is a batch, department battery, or variant series where smooth previews multiply total render time.
- The user only asked to test or sketch the concept, so a stepped preview may answer the question faster.

Do not stop to ask when the user explicitly asks for smooth animation, when the estimated frame count is modest, or when smooth motion is essential to the truth of the concept and render time is reasonable.

When asking, offer the tradeoff plainly: a fast stepped version for structure and QA, or a smoother version that takes longer to compile/render. If proceeding without asking, record the reason in the QA note.

## Memory and Stitching Fallback

If a smooth animation with many repeated objects hits TeX memory limits, do not immediately abandon the intended motion. First reduce truly redundant detail, such as vector-field density or duplicated labels. If the concept still needs many frames, split the animation into shorter frame decks and stitch the rendered GIF/MP4 segments.

Use stitching when:

- A full animation fails with TeX capacity or main-memory errors.
- The visual field is heavy but each stage is independently renderable.
- The user needs a smooth preview more than a single monolithic `animate.sty` source.

Preserve a shared macro/source file for consistency across segments. Render each segment to PNG frames or GIF with `render_animation_preview.py`, then concatenate in order with `ffmpeg` or ImageMagick. Record in the QA note that the preview was stitched and whether the interactive PDF is segmented, simplified, or unavailable.

## Pacing Gate

Before rendering, map semantic states to presentation frames. Do not assume one semantic state should equal one displayed frame.

- Start with a meaningful first frame. Avoid title-only or blank opening frames unless the pause itself teaches something.
- Hold simple highlights for about 0.5--1 second.
- Hold new structure, new labels, or a new visual grammar for about 1--1.5 seconds.
- Hold dense states such as payoff tables, multiple branches, legends, final takeaways, threshold crossings, or completed mechanisms for about 1.5--3 seconds.
- Use repeated pages or repeated semantic states when `animate.sty` needs unequal dwell times. Keep the frame-preview source synchronized with the interactive source so GIFs and contact sheets reveal the real pacing.
- Slow down or split the animation when a viewer would need to compare three or more newly introduced elements at once.
- Record the fps, semantic-state sequence, and any long holds in the QA note.

## TeXample Sources

Use these URLs when a user asks to fetch or adapt more animation examples:

- Animation category: https://texample.net/category/topics/animations/
- Animated definite integral: https://texample.net/animated-definite-integral/
- Lower Riemann sum: https://texample.net/lower-riemann-sum/
- Upper Riemann sum: https://texample.net/upper-riemann-sum/
- Andler optimal lot-size: https://texample.net/andler-optimal-lot-size/
- Convolution of two functions: https://texample.net/convolution-of-two-functions/
- Towers of Hanoi: https://texample.net/towers-of-hanoi/
- Projectile: https://texample.net/projectile/
- Animated distributions: https://texample.net/animated-distributions/

Treat these as behavior and design patterns, not as code to copy wholesale. Preserve attribution in QA notes when a source pattern materially shaped the output.

## Pattern Adaptation

- **Integral or Riemann-sum pattern**: adapt to accumulated economic area, welfare, exposure, or coverage. Keep the moving boundary and shaded area clear.
- **Lot-size or parameter-sweep pattern**: adapt to business tradeoffs where a candidate decision moves across a cost, risk, or response curve.
- **Convolution or overlap pattern**: adapt to mechanisms where an outcome is generated by shared support, matching, weighted overlap, or combined shocks.
- **Hanoi or recursive-state pattern**: adapt to discrete transfers among states. Keep the state grammar clean; do not add unrelated metrics into the same render.
- **Projectile or trajectory pattern**: adapt to a moving path relative to a target, limit, threshold, or reference line.
- **Animated-distribution pattern**: adapt to changing parameters, uncertainty, policy simulations, or sampling distributions. Prefer direct labels and external captions.
- **Delayed-adjustment / J-curve pattern**: adapt to trade-balance J-curves, campaign wear-in, product adoption, process learning curves, drawdown-and-recovery paths, or policy response lags. Keep the intervention date, baseline, and time axis fixed; reveal the path smoothly only when the lag, reversal, or catch-up is the point. Use holds at the intervention, trough/overshoot, and final state.
- **Paced-cycle pattern**: adapt to business cycles, adoption cycles, inventory loops, risk cycles, or phase diagrams where the background context stays fixed and a highlighted state travels around the loop. Use `templates/animation_paced_cycle.tex` as a starting point, and hold named states longer than in-between transitions.
- **Smooth-cycle-fill pattern**: adapt paced-cycle diagrams when the viewer should perceive continuous traversal or accumulated progress around the loop. Use `templates/animation_smooth_cycle_fill.tex`; keep explanatory labels stable within regimes and let the marker/path move smoothly.
- **Threshold-corridor trajectory pattern**: adapt to belief spaces, survival regions, feasible sets, safety corridors, control limits, or policy bands. Keep regions and thresholds fixed; reveal the trajectory smoothly; only reveal exit/failure markers after the crossing; hold the terminal crossing state long enough to read.

## Output Contract

For each animation, prefer:

- interactive `.tex` using `animate.sty`
- compiled interactive `.pdf`
- first-frame `.png` from `compile_render.py`
- visual QA JSON from rendered PDF checking
- frame-preview `.tex` or equivalent static frame deck
- frame-preview `.pdf`
- GIF or MP4 preview for local chat/app inspection
- contact sheet of key frames when reviewing several animations
- short design or QA note with source pattern, why animation was warranted, fps/hold strategy, checks run, and repairs

PDF animation interactivity depends on the viewer. A successful `animate.sty` PDF can still need a GIF/MP4 preview or key-frame contact sheet for visual inspection in environments that do not play PDF annotations.

Use `scripts/render_animation_preview.py` for frame-preview PDFs when possible. It renders pages to PNG frames, discovers actual frame filenames and zero-padding, makes a GIF, makes a contact sheet, and writes a small manifest. Do not hard-code `pdftoppm` frame names such as `frame-01.png` or `frame-1.png`; installations differ.

## Verification

1. Run static safety checks on both the interactive source and the frame-preview source.
2. Compile the interactive source and run rendered visual QA.
3. Render a frame deck or selected key frames.
4. Inspect first, middle, final, and semantic edge frames.
5. Inspect the GIF/MP4 preview at intended speed; patch pacing if the viewer cannot absorb the changes.
6. Patch severe visual defects: title-band collision, text overlap, clipped labels, crowded arrows, or unreadable annotations.
7. Patch semantic defects: labels that appear in the wrong frame, moving elements with no meaning, incorrect threshold/buffer logic, or a final state that contradicts the teaching message.
8. Save versioned outputs during critique so stale image caches cannot hide a changed render.

Check semantic edge frames: labels and highlights should appear only when true, such as `overlap` only during overlap, `breach` only after breach, or `target met` only once the target is reached.

## Animation-Specific Critique

Record one outcome: `keep`, `simplify`, `split`, or `reject`.

Ask:

- Does the motion explain a mechanism, transition, accumulation, sweep, or risk?
- Would three static panels be clearer?
- Does any label become false in some frames?
- Does a moving annotation collide with fixed labels at any point?
- Does the first frame make sense on its own?
- Does the final frame communicate the promised lesson?
- Is the playback speed plausible for the audience and context: lecture explanation, self-paced PDF, research talk, or quick preview GIF?

General overcrowding rule: when a prompt combines different figure grammars, split or simplify by default. Examples include state transfer plus effect estimates, causal graph plus funnel, distribution animation plus regression table, or mechanism diagram plus diagnostics. The marketing cohort example is one instance of this broader rule: the useful animation was state transfer, while mediation paths and effect estimates belonged in separate figures or external notes.
