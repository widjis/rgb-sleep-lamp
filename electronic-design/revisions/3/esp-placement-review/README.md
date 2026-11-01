# ESP-12F placement review

Status: LAYOUT_REVIEW; routing not started.
17 supporting components moved via the live KiCad IPC MCP and saved natively.
U1, all mounting holes, outline, RF keepout, U2/U3/U4 and other power parts retained.
C1/C2 near VCC; boot/reset/enable resistors near their pins; J2 UART on left;
J6/J7 GPIO/control headers flank the region; SW1/SW2 accessible above U1.
All parts remain on F.Cu: underside not required for this pass. C2 uses 45 degrees.

Pin/net identity unchanged for all 146 pads. Native saved PCB reloaded through
KiCad pcbnew for verification; all moved pad centers inside outline.
Native DRC with refill and schematic parity: no clearance, edge, courtyard,
silkscreen or parity errors. Four footprint/library mismatch warnings remain
on R1/R2/R4/R5 and are not signed off. 104 unconnected items remain (unrouted).
Native SVG was rendered locally and visually reviewed. Header mating, assembled
case fit, RF, thermal and electrical functionality were not physically tested.
Placement distances in verification.json are straight-line pad center distances,
not routed lengths or return-loop measurements. No tracks or vias added.

The before/after placement ledger is in verification.json; the pre-placement PCB
backup is in ../backups/before-esp-placement-20261027-044117/.

At final live read-back, C1 and C2 had subsequently changed in the editor. Their latest coordinates are recorded in verification.json, retained without overwrite; the saved DRC/preview above describe the earlier saved placement, not those subsequent live edits.
