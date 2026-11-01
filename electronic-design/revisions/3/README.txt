RGB SLEEP LAMP E3 - BARE MP1584EN / PASSIVES PARKED

ICs and semiconductor devices U1-U4,D1,D2 inside outline. R/C/L/fuse/connectors/switches outside for manual placement. H1-H3 remain fixed. No routing; not fabrication ready.

U3 wired module interface removed. buck.kicad_sch now shows bare MP1584EN SOIC8E and external L/D/R/C, intended on main PCB. PDC00420V remains a separate selected USB-C module on J4.

U3 pinout:1SW,2EN,3COMP,4FB,5GND,6FREQ,7VIN,8BST,9EP GND. SOIC8E EP2.62x3.51 footprint follows manufacturer recommended land pattern. Verify actual donor marking/package.

REFERENCE VALUES, NOT REVERSE-ENGINEERED DONOR VALUES:
L1=15uH >=3.5A; FB210k/40.2k =>4.979V nominal; COMP100k+150pF; FREQ100k ~900kHz; EN100k/24.9k; BST100nF; VIN10uF50V; output22uF10V.
R/C/diode/inductor footprints are provisional. If donor says4R7 it is4.7uH, not15uH. Measure actual values/packages before desoldering or committing footprints. Existing C5 470uF bulk requires checking COMP, ESR, startup and load stability. No bench qualification.

When placing passives, bring C11,D2,L1,C12 and COMP/FB parts close to U3, keep high-current loops short and FB away from SW. Ground EP to adequate copper. The requested active-only state intentionally does not yet satisfy final placement requirements.
Minimum track0.2mm, viaOD0.4mm retained. Native resave all3sheets, native PCB SaveBoard/reload. ERC0, geometry0, parity0;104unconnected expected. E2 preserved.
