# Routing rules

Applied using KiCad native Board Setup and settings import; saved in circuit.kicad_pro.
Live MCP net class read-back confirms all six classes.

Minimum clearance 0.20 mm; track and connection neck 0.20 mm; copper to edge
0.50 mm; copper to unrelated hole 0.25 mm; hole to hole 0.25 mm.
Via minimum OD/drill 0.60/0.30 mm; annular ring minimum 0.15 mm.
Via presets 0.60/0.30 and 0.80/0.40 mm. Silk clearance 0.15 mm,
text height/thickness minimum 0.80/0.10 mm. No microvia process is specified;
the two-layer board is intended for ordinary through vias.

Preferred widths: signals 0.25, 3V3 0.50, 20V/VIN_BUCK 0.80, SW 1.00,
5V/GND 1.50 mm. These are routing preferences, not certified ampacity or
per-net hard minimums. Short pad escapes may use smaller selected presets,
never below 0.20 mm, before widening. Use copper fills where appropriate,
keep the SW region local, and account for actual copper thickness/current,
voltage drop and thermal conditions. GND should normally use a continuous
plane; no plane or route was added in this task.

DRC after settings: 0 geometry violations, 0 schematic parity issues,
6 existing footprint/library warnings, 104 unconnected items (unrouted).
No manufacturing supplier or copper stackup was newly assumed/qualified.
Backups are in ../backups/before-routing-rules-20261027-061243/.
