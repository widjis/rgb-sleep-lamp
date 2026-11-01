ESP-12F minimum system

J1: 1=3.3V, 2=GND. Regulated supply capability >=500mA; no 5V input.
J2: 1=GND, 2=ESP RX (connect adapter TX), 3=ESP TX (connect adapter RX), 4=RESET_N (optional; leave open for manual reset).
Use UART TTL 3.3V; never connect real RS-232 directly.
CH340 / CP2102 / FT232 or an ESP32 UART bridge can work if firmware, levels and wiring are correct.
Do not connect a second active TX driver onto the same UART net.
Hold FLASH, press/release RESET, release FLASH; upload firmware. Press RESET after upload.
R1-R5=10k; C1=100nF; C2=10uF. Input capacitors close to VCC/GND.
D1: efficient red LED; R6=2.2k. At 3.3V and Vf=2.0V, I~0.59mA, R power~0.77mW. For rail 3.0-3.6V, Vf 1.8-2.2V, R +/-5%: I~0.35-0.86mA, max R power~1.55mW; budget up to 20.7mAh/day. Exact LED visibility and Vf need actual part validation.
ERC: 0 violations using native KiCad 10.0.7 CLI. Netlist exported for connectivity check.
Unused GPIO and internal flash pins marked NC in this stage; remove NC when expanding circuit.
Existing ESP-12E footprint assignment retained for ESP-12F; physical module variant must be checked before PCB manufacture.
PCB not updated/routed; no physical upload, power or RF testing performed.
Close/reopen schematic without saving an older editor buffer over the new file.
