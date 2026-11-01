# Power placement review

Status: LAYOUT_REVIEW, unrouted. Twenty-two components moved; no tracks or vias added.
The latest live ESP/user placement was captured before editing and preserved.
All placed components are on F.Cu. Board outline, RF keepout and mounting unchanged.

## Groups
- J4/F1: PDC004 20V wire input and series fuse near USB side.
- U3/D2/L1/C11/C12/C3/C4: MP1584 input bypass, bootstrap, switch diode,
  inductor and input/output storage. VIN ceramic and diode local to regulator.
- R10/R11: feedback; R12/C13: compensation; R13: frequency; R14/R15: EN.
  Signal network below/to the side of the IC, separated from upper SW region.
- U4/C7/C8/C9: LDO and input/output capacitors below buck, closer to ESP.
- C5/J3: bulk 5V storage near LED output solder pads on left side.
- C10/R7/R8 belong to the LED data buffer, kept parked for a separate pass.

## Routing notes for the user
1. Start buck high-current paths: C11 VIN/GND, U3, D2, L1, C4. Keep the hot
   loop compact and SW copper local; do not route FB/COMP under L1/SW.
2. Bootstrap C12 goes directly between BST and SW. Take feedback from output
   near C4, away from diode/inductor switch copper, with quiet ground return.
3. Provide an exposed-pad GND/thermal copper return for U3. U4 tab/pin 2 is
   +3.3V (not GND); reserve copper for its heat spreading on that net.
4. C7 is LDO input, C8/C9 LDO output. Route the 3V3 supply to ESP decoupling
   without passing through LED power return. Route LED 5V/GND for actual load.
5. Retain project routing limits: track >=0.20mm, via copper OD >=0.40mm;
   power widths need actual current/thermal assessment. Do not add copper,
   traces or parts into the ESP antenna keepout on either side.

## Evidence and limitations
Native saved file reloaded and checked: 146 pad/net identities unchanged;
all moved pad centers inside outline; zero tracks and vias. Native DRC with
refill and schematic parity: zero geometric violations and parity issues;
104 unconnected items remain. Six existing footprint-library warnings remain
on R1/R2/R4/R5/R9/J5, same as live baseline. These were not silently excluded.
Native SVG rendered and visually checked; distances in verification.json are
pad-center distances, not routed lengths or electrical performance proof.
Mechanical assembled fit, heights, thermal, EMI/RF and physical electronics
not tested. Donor IC, diode and inductor package/value labels remain provisional.

IPC full-footprint updates with the installed kicad-python 0.7.1 were observed
to drop 3D model references and a polygon point. For this handoff, power
footprints were restored from the native pre-edit baseline with the approved
positions applied by pcbnew, then the live editor was reloaded and saved via
IPC. Model counts are verified preserved, and new mismatch warnings removed.
Future IPC placement edits require footprint-integrity checks, not just position
read-back. The original baseline and interim IPC output are backed up.

Sources: MPS MP1584 datasheet, PCB Layout Guide:
https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP1584/document_id/204
