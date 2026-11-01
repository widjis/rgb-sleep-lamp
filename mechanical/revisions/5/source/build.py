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
        if part.id=='diffuser' and feature.id=='shade_inner':
            feature=feature.model_copy(update={'size':['46.7','144.4','1']})
        tool=primitive(feature,values)
        result=tool if result is None else (result.fuse(tool) if feature.operation=='add' else result.cut(tool))
        result=result.clean()
    parts[part.id]=result
# Matched top fillets: original roof underside z=143.8, roof top z=145.
s=parts['diffuser']
def circular_at(shape,z):
    return [e for e in shape.Edges() if e.geomType()=='CIRCLE' and abs(e.BoundingBox().zmin-z)<0.0001 and abs(e.BoundingBox().zmax-z)<0.0001]
s=s.fillet(6.0,circular_at(s,145.0))
# 0.8 mm optical wall and roof; concentric inner/outer top curves.
s=s.fillet(5.2,circular_at(s,144.2))
parts['diffuser']=s.clean()

# Real RH single-start thread, built from rotating radial section wires.
import math
pitch=3.5
root=44.4
crest=45.4
def cyl(r,h,z=0): return cq.Solid.makeCylinder(r,h,cq.Vector(0,0,z))
def bounded_intersection(a,b):
    result=a.intersect(b)
    assert -0.001 <= result.Volume() <= min(a.Volume(),b.Volume())+0.001, 'Boolean intersection volume bound'
    return result
def ridge(extra=0):
    wires=[]
    # Exact screw-law sections; smooth loft creates non-analytic helical faces.
    for i in range(193):
        angle=6*math.pi*i/192
        z=-pitch+pitch*angle/(2*math.pi)
        profile=[(44.1,z-1.3-extra),(crest+extra,z-.3-extra),
                 (crest+extra,z+.3+extra),(44.1,z+1.3+extra)]
        pts=[cq.Vector(r*math.cos(angle),r*math.sin(angle),h) for r,h in profile]
        wires.append(cq.Wire.makePolygon(pts+[pts[0]]))
    result=cq.Solid.makeLoft(wires,ruled=False)
    assert result.isValid() and result.Volume()>1
    return result
raw=ridge()
clipped=bounded_intersection(raw,cyl(50,6))
assert clipped.Volume()>1
# Local root reinforcement inward, without changing the electronics cavity.
male=cyl(root,6).fuse(clipped).cut(cyl(43.0,7,-.5)).clean()
# Cut upper lead-in with an annular cutter rather than tangent envelope intersection.
lead=cyl(50,.7,5.3).cut(cq.Solid.makeCone(45.5,44.4,.7,cq.Vector(0,0,5.3)))
male=male.cut(lead).clean()
outside=male.cut(cyl(root,8,-1))
assert outside.Volume()>1, 'Missing male helical material'
parts['base']=parts['base'].fuse(male.translate((0,0,35))).clean()
# Thread region unchanged internally; connect reinforcement to the thinner shell.
female_blank=parts['diffuser'].fuse(cyl(46.9,6).cut(cyl(44.7,6))).clean()
# Short 45-degree internal transition above thread, not global thickening.
transition=cyl(46.9,2,6).cut(cq.Solid.makeCone(44.7,46.7,2,cq.Vector(0,0,6)))
female_blank=female_blank.fuse(transition).clean()
# Clip cutter axially away from its radial extremes; never tangent at crest.
cutter=bounded_intersection(ridge(.3),cyl(50,6))
female=female_blank.cut(cutter).clean()
removed=female_blank.Volume()-female.Volume()
assert removed>1, 'Female groove removed no material'
female=female.cut(cq.Solid.makeCone(45.7,44.7,.7)).clean()
parts['diffuser']=female
counts={}
for key in ('base','diffuser'):
    counts[key]=sum(f.geomType()=='BSPLINE' for f in parts[key].Faces())
    assert counts[key]>0, 'Missing helical BSPLINE faces '+key
checks=[]
for t in (0,.25,.5,1,1.5):
    mating=female.rotate((0,0,0),(0,0,1),360*t).translate((0,0,35+pitch*t))
    overlap=bounded_intersection(parts['base'],mating).Volume()
    checks.append([t,overlap])
    assert abs(overlap)<.01, 'Assembly interference '+str(checks)
report={'pitch_mm':pitch,'male_root_major_diameter_mm':[88.8,90.8],
        'female_bore_groove_diameter_mm':[89.4,91.4],
        'radial_clearance_mm':.3,'axial_profile_allowance_mm':.3,
        'collar_height_mm':6,'collar_root_wall_mm':1.4,
        'female_groove_back_wall_mm':1.8,
        'bspline_faces':counts,'male_outside_root_mm3':outside.Volume(),
        'female_groove_removed_mm3':removed,'assembly_overlap_samples_mm3':checks}
print('THREAD_CHECKS',json.dumps(report))
(ROOT/'thread_checks.json').write_text(json.dumps(report,indent=2))
for key,s in parts.items():
    if not s.isValid() or len(s.Solids())!=1: raise ValueError('Invalid solid '+key)
    cq.exporters.export(s,str(ROOT/(key+'.stl')))

for part_id,shape in parts.items():
    cq.exporters.export(shape,str(ROOT/(part_id+'.step')))
