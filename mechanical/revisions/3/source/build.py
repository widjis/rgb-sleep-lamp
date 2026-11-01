# Forma native CadQuery workspace. Units mm. Preserve existing IDs and geometry.
import json
from pathlib import Path
import cadquery as cq
from backend.schema import Spec
from backend.cad_worker import primitive
ROOT=Path(__file__).parent
SPEC=Spec.model_validate(json.loads((ROOT/'baseline.json').read_text()))
values={p.id:p.value for p in SPEC.parameters}
if (ROOT/'config.json').exists(): values.update(json.loads((ROOT/'config.json').read_text()))
parts={}
for part in SPEC.parts:
    result=None
    for feature in part.features:
        if part.id=='base' and (feature.id in ('shade_seat','seat_center') or feature.id.startswith('shade_pilot_')): continue
        if part.id=='diffuser' and feature.id.startswith('shade_clearance_'): continue
        tool=primitive(feature,values)
        result=tool if result is None else (result.fuse(tool) if feature.operation=='add' else result.cut(tool))
        result=result.clean()
    parts[part.id]=result
# Matched top fillets: original roof underside z=143.8, roof top z=145.
s=parts['diffuser']
def circular_at(shape,z):
    return [e for e in shape.Edges() if e.geomType()=='CIRCLE' and abs(e.BoundingBox().zmin-z)<0.0001 and abs(e.BoundingBox().zmax-z)<0.0001]
s=s.fillet(6.0,circular_at(s,145.0))
s=s.fillet(4.8,circular_at(s,143.8))
parts['diffuser']=s.clean()

# Coarse RH single-start joint; local assembly delta Z=35 mm.
pitch=3.5
def cyl(r,h,z=0): return cq.Solid.makeCylinder(r,h,cq.Vector(0,0,z))
def ridge(extra=0):
    # Profile translated radially as a whole for female clearance.
    z=-3.5
    pts=[(44.25+extra,z-1.3-extra),(45.4+extra,z-.3-extra),
         (45.4+extra,z+.3+extra),(44.25+extra,z+1.3+extra)]
    path=cq.Wire.makeHelix(pitch,14,44.4,center=cq.Vector(0,0,z))
    return cq.Workplane('XZ').polyline(pts).close().sweep(cq.Workplane(obj=path),isFrenet=True).val()
male=cyl(44.4,6).fuse(ridge().intersect(cyl(45.4,6))).cut(cyl(43.6,7,-.5)).clean()
env=cyl(45.4,5.3).fuse(cq.Solid.makeCone(45.4,44.3,.7,cq.Vector(0,0,5.3)))
male=male.intersect(env).clean()
parts['base']=parts['base'].fuse(male.translate((0,0,35))).clean()
female=parts['diffuser'].fuse(cyl(46.4,6).cut(cyl(44.7,6))).clean()
female=female.cut(ridge(.3)).cut(cq.Solid.makeCone(45.7,44.7,.7)).clean()
parts['diffuser']=female
checks=[]
for t in (0,.25,.5,1,1.5,2):
    mating=female.rotate((0,0,0),(0,0,1),360*t).translate((0,0,35+3.5*t))
    v=parts['base'].intersect(mating).Volume()
    checks.append([t,v])
print('THREAD_CHECKS',checks)
for key,s in parts.items():
    if not s.isValid() or len(s.Solids())!=1: raise ValueError('Invalid solid '+key)
    cq.exporters.export(s,str(ROOT/(key+'.stl')))

for part_id,shape in parts.items():
    cq.exporters.export(shape,str(ROOT/(part_id+'.step')))
