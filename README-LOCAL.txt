RGB Sleep Lamp - local hardware workspace

Mechanical design: mechanical/
  current/ -> mechanical revision R9 (STEP/STL and original CadQuery source)
  freecad/RGB Sleep Lamp.FCStd -> FreeCAD working document
Electronic design: electronic-design/
  current/ -> KiCad lamp electronics E2 (USB-C only, unrouted)
  planning/ -> historical mechanical planning; current E2 documentation is in electronic-design/current/README.txt
Documentation: documentation/ (checks,attachments,backups and archived metadata)

Root revisions,electronics,checks,attachments,backups and current-* entries are compatibility links; use mechanical and electronic-design for new work. All original files preserved and hash-verified during folder split.

FreeCAD mechanical case starts from imported R9 STEP solids, not automatically reconstructed sketch history. Reference PCB is mechanical geometry only. Current PCB E1 is still old larger baseline; proposed circular board is only a template.

Power direction: external USB-C PD20V activator ->buck5V forWS2812B strip ->regulator3.3V forESP. No20V directly toLED/ESP, no220V inside casing.30LEDs on50cmstrip60/m; helix pitch40mm concept on62mmcore.

R9 diffuser still needs support at externalR6/thread despite local45degree blend. Fit/thermal/physical print unverified. Old CadQuery source imports ai-cad-studio backend helpers; preserved as history, not standalone FreeCAD source.

Electronics E2: USB-C PDC00420V, wired MP1584 module set5V, AMS1117-3.3, ESP12F, AHCT LED buffer. E1 preserved. E2 uses current FreeCAD PCB contour and3mount holes, with no tracks. Open electronic-design/current/circuit.kicad_pro; see current/validation.json. E2 ESP placement supersedes earlier MCAD placement study; ESP envelope synchronized. Other critical parts still need actual dimensions and full3D/thermal/RF validation.

Electronics E3: bare MP1584EN reference circuit, semiconductors inside outline, passives/connectors/switches parked outside. Donor values/packages TBD. Open electronic-design/current/circuit.kicad_pro.

E5 UPDATE (2026-10-31): electronic-design/current -> revisions/5. All routing rebuilt; track/clearance >=0.3 mm; via DRILL 0.8 mm / outside copper 1.2 mm. Native DRC/parity/unconnected 0, all DRC checks active. Final board/render/fabrication evidence in E5 validation.json. E4 remains intact.
