RGB SLEEP LAMP - ELECTRONIC REVISION E2
STATUS: PLACEMENT_REVIEW_UNROUTED; not fabrication-ready.

Open circuit.kicad_pro. Controller and power/LED driver are two schematic sheets.
E1 remains preserved in revisions/1. No GPS Tracker source project was modified.

Removed: IP2312 charger, battery/NTC connectors, MT3608 boost, charge/full LEDs,
associated inductors/diode/resistors/caps and battery disconnect switch.
Retained: ESP-12F boot network, RESET/FLASH buttons, UART programmer, 3V3 test
header, expansion GPIO/control headers and labeled 3V3 power LED.

Power: external PDC004 fixed20V -> J4 -> F1 1A >=32V -> MP1584 MODULE U3,
set to5.00V -> LED strip and AMS1117-3.3 -> ESP. No battery and no AC mains.
PDC004 USB-C is POWER ONLY, not a USB-to-UART programmer.
J4 pads are OUT+/OUT- wire connections from PDC004, not a bare USB-C socket.
U3 is a complete22x17mm-class MP1584 MODULE, not a bare IC. Its four PCB pads
are wire landing points, not assumed physical solder registration with donor pads.
Actual module dimensions, wire routing, insulation and positive retention TBD.

New LED path: GPIO4 -> 74AHCT1G125 (5V, OE tiedGND) ->330ohm -> J3 DIN.
100k pulldown holds buffer input low during boot. 100nF close to buffer.
470uF10V bulk capacitor near LED output. J3:1=5V,2=DIN,3=GND.
Case button: GPIO5 active-low on J5,10k pullup. J5:1=GPIO5,2=GND.
J6 pins3/4 share these functions; do not attach another driver/I2C bus there.
Unused GPIO12/13/14/16 remain available. ADC at module is0-1V, not3V3.
UART J2:1 GND,2 RX(ESP)<-adapterTX,3 TX(ESP)->adapterRX,4 RESET_N.
Do not connect adapter supply to 3V3 test header while lamp is powered.

Power budget assumption:30LED x60mA=1.8A; reserve0.5A for controller, about2.3A
on5V bus. Target buck2.5A, but a module's3A marketing rating is NOT proof of
continuous operation in a closed printed case. Test full white, startup/ripple,
5V sag, WiFi bursts and temperature. AMS1117 dissipates0.34W at200mA and0.85W
at500mA. Verify actual donor's pinout, output-cap ESR and copper cooling.
Use a USB-PD source with a20V PDO and adequate current; fallback5V cannot be
assumed to give a regulated5V buck output. Verify output voltage before wiring.

PCB: latest FreeCAD outline with USB support tongue, rounded transitions,
three M3 clearance holes diameter3.2mm at MCAD radius29 angles60/180/300.
KiCad origin100,100; mapping x=100+MCADx, y=100-MCADy. Original B-spline
blends approximated with maximum0.005mm chord deflection; circular arcs native.
Board is2-layer1.6mm. ESP moved to lower edge to clear the deep case-post notches.
ESP antenna copper keepout exists on both copper layers. Only the ESP MCAD
placeholder was synchronized; full populated-board 3D fit and RF performance
are not validated. No fabricated component/package dimensions assumed from renders.

Routing is intentionally empty. Ratsnest/unconnected report is expected.
Minimum track0.20mm, via OD0.40mm, copper clearance0.20mm, edge0.50mm.
Default via0.60/0.30mm. Power netclass widths are starting values, not thermal proof:
5V/GND1.5mm,3V3 0.5mm,20V0.75mm. Use short wide5V/GND pours and short data return.
Assembly references are on F.Fab during placement review. Power/LED pad labels
are on F.Silkscreen. ESP antenna outline is on F.Fab to avoid printing outside PCB.

Validation: see validation.json, erc.json, drc.json and schematic.pdf.
Native schematic CLI resave and PCB SaveBoard/reload performed. ERC/net assertions
and PCB geometry/parity checked. No routing, Gerbers, physical/thermal/RF testing
or production approval.
