RGB Sleep Lamp - independent local hardware workspace

Project moved out of Forma managed data on 2026-10-26. Continue work directly here. No application source or unrelated projects changed. The old managed-data path no longer exists; close/reload stale Forma project tabs and do not start jobs against the old project.

Current mechanical R9: current-mechanical/ -> revisions/9/ (STEP,STL,source,checks).
Current electronics E1: current-electronics/ -> electronics/revisions/1/ (circuit.kicad_pro,schematics,PCB,library).
Full history: revisions/ and electronics/revisions/.
PCB outline proposal and30LED spiral plan: checks/r9-pcb-and-led/.
All original source/history/files preserved and hash-verified; see relocation-manifest.json.

Power direction from user: USB-C PD activator configured20V. This is a planning decision, NOT implemented in E1. Design chain: compatiblePDadapter/cable ->20Vtrigger ->buck5V forWS2812B ->3.3V regulator forESP. Never feed20V directly toLED/ESP. Confirm actualtrigger/adapter profile andbuck current/thermal capabilities before selecting components. No220V inside lamp.

Geometry remains R9: PCB seats4posts for62mm board; diffuser45degree transition plusR0.3. Slicer still~28.5gsupport due remainingR6/thread overhangs. No new geometry changes in relocation.

Source build.py imports backend.schema/backend.cad_worker from existing ai-cad-studio runtime. Moving files does not make that source standalone. STEP/STL and KiCad native artifacts are present; before future source rebuild, use a controlled local environment and resolve these dependencies without resuming Forma orchestration.
