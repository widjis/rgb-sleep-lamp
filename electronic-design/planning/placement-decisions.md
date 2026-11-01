# Placement concept
Selected: USB +Y at existing power opening; ESP-12F -X with antenna over the host PCB edge; buck right/center; 3V3 and LED-data logic lower center.
Alternatives considered: (A) +Y existing opening, selected for retained access; (B) -Y rejected because it uses the existing button side and needs another opening; (C) +X rejected because it conflicts with a tall cover post.
ESP module envelope24x16x3mm from Ai-Thinker. Gold antenna end is an approximate6mm visual reference, not verified PCB artwork. No-copper RF study is provisional; final footprint keepout and installed RF performance remain unverified.
ZY12PDN solder-pad variant nominal31x15x4mm from Joy-IT. Indonesia listing found on Shopee; stock and exact variant not measured. EasyWare offers another 5-20V trigger, price Rp34,200 at lookup; not assumed dimensionally identical.
USB module is a daughterboard above main board (bottomZ14.8); USB provisional port bottomZ15 at +Y opening. Final socket datum, plug shell, strain relief and positive module retention require actual module dimensions. It is not floating-ready for manufacture.
PCB six notch intersections have R3 fillets. Hole pattern38x32mm; base support posts relocated together, M3x4x4 insert pocket provisional. Four driver clearance cylinders radius3.2mm have0 overlap with reserved component envelopes.
The previous R9 STEP/STL files are archived history. Use mechanical/freecad/base-current.step and base-current.stl for the revised mounting positions; original R9 base has the old hole pattern. Electronic E1 is unchanged.
CAD board/insertion/component/cover checks passed for the simplified envelopes. No routing, thermal, RF, physical fit or production approval.

## Three-screw update (supersedes four-hole pattern)
Three diameter3.2mm holes on radius29mm, angles60/180/300deg, centered between the three base cover posts at0/120/240deg. Base supports relocated with matching insert pockets; old four PCB supports removed. ESP/RF envelopes rotated30deg aroundZ to free left screw access. CAD board/base, vertical insertion, simplified component/base and three driver cylinders all0mm3 overlap. KiCad E1 unchanged.

## Selected USB module
User selected EasyWare PDC004 fixed20V SKU EP004131, replacing ZY12PDN. Supplier specifies solder OUT+/OUT-, but no reliable mechanical drawing. Reserve18x11x5mm (overall PDC004 variants online), provisional. +Y port position retained. CAD reserve/base overlap0mm3. Final holder and socket datum require actual dimensions. Power chain remains20V to buck5V then3V3.

## USB-C support tongue
Main PCB locally extended at +Y:16mm wide, frontY41.8mm, R2 blends. Remaining contour retains5mm inward offset. Three mounting holes unchanged. CAD PCB/base and vertical insertion sweep0mm3. Board overall Y78.8mm. PDC004 reserved daughterboard bottomZ14.8 vs main PCB topZ12 leaves2.8mm spacer gap. Module front/connector region projects2.2mm beyond main-board tongue; final retention and module datum TBD after measurement. Updated pcb-space-outline.step is mechanical reference, E1 unchanged.
