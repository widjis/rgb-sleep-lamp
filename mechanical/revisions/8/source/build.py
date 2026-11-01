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
# Top-access redesign. Original base coordinates retained for assembly checks.
# Orientation inspiration only: alpaco.it Electronics Enclosure Generator
# https://www.alpaco.it/generators/case/ : open-side-up housing, separate lid.
# No reference geometry copied. Electronics files/metadata are not touched.
original_parts=dict(parts)
old_volumes={k:v.Volume() for k,v in parts.items()}
# Transfer the exact existing roof, mount bores and male collar.
deck=bounded_intersection(parts['base'],cyl(50,9,32)).translate((0,0,-32)).clean()
housing=cyl(47.5,36.4,-2.4).cut(cyl(45.1,36,0)).clean()
# Integral 2.4 mm floor, housing rim at z34; deck underside assembles at z32.
# Deck's recessed perimeter receives the housing's positive locating rim.
deck=deck.cut(cyl(50,2).cut(cyl(44.8,2))).clean()
# Three floor-grown posts: no suspended boss ledges. 45-degree additive roots.
centers=[]
for i in range(3):
    a=2*math.pi*i/3
    x,y=40*math.cos(a),40*math.sin(a)
    centers.append((x,y))
    post=cyl(6,32).translate((x,y,0))
    root_support=cq.Solid.makeCone(8,6,2,cq.Vector(x,y,0))
    housing=housing.fuse(post).fuse(root_support).clean()
# Restrict reinforcement to the existing outer envelope, never add cavity material.
unclipped_housing=housing
housing=bounded_intersection(unclipped_housing,cyl(47.5,40,-3)).clean()
assert housing.cut(unclipped_housing).Volume()<.001, 'Clipping invented material'
assert housing.Volume()<=unclipped_housing.Volume()+.001
# All material inside the envelope, including insert walls and roots, retained.
assert unclipped_housing.cut(housing).intersect(cyl(47.499,40,-3)).Volume()<.001
envelope_removed=unclipped_housing.Volume()-housing.Volume()
assert 0<envelope_removed<100, 'Unexpected clipping volume'
assert housing.BoundingBox().xlen<=95.001 and housing.BoundingBox().ylen<=95.001
assert housing.isValid() and len(housing.Solids())==1
# Reapply exact original side-port cutters after adding posts.
base_spec=next(p for p in SPEC.parts if p.id=='base')
for f in base_spec.features:
    if f.id in ('power_opening','button_opening'):
        housing=housing.cut(primitive(f,values)).clean()
for x,y in centers:
    # Provisional 3.70 mm pocket for nominal OD4 x L4 M3 heat-set insert.
    # 4.5 mm depth; insert installed flush at z32. Coupon required.
    housing=housing.cut(cyl(1.85,4.6,27.5).translate((x,y,0)))
    housing=housing.cut(cq.Solid.makeCone(1.85,2.15,.3,cq.Vector(x,y,31.7))).clean()
    deck=deck.cut(cyl(1.7,3.2,-.1).translate((x,y,0)))
    deck=deck.cut(cq.Solid.makeCone(1.7,2,.3,cq.Vector(x,y,2.7))).clean()
    # Vertical tool approach available after removing diffuser.
    approach=cyl(3,20,32.01).translate((x,y,0))
    assert bounded_intersection(housing,approach).Volume()<.001
# Two pry slots in housing rim, open to exterior and top.
# 8 mm tangential width, 1.2 mm deep; finger/tool lifts deck edge.
for angle in (60,240):
    notch=cq.Workplane('XY').box(8,7,1.2,centered=(True,True,False)).val()
    notch=notch.translate((0,46,32.8)).rotate((0,0,0),(0,0,1),angle)
    housing=housing.cut(notch).clean()
# Small top-entry chamfers on retained LED mount and wire bores.
for x,r in ((0,3.3),(26,1.7),(-26,1.7)):
    deck=deck.cut(cq.Solid.makeCone(r,r+.25,.25,cq.Vector(x,0,2.75))).clean()
# Corrected architecture: collar belongs to base; no removable threaded deck.
# Reuse documented Alpaco orientation lesson only, adapted to fixed collar.
housing=cyl(47.5,34.3,-2.4).cut(cyl(45.1,33,0)).clean()
# Continuous tapered wall, underside inward rise 3.1 / run 2.1 = 55.9 degrees.
transition_wall=cq.Solid.makeCone(47.5,44.4,3.1,cq.Vector(0,0,31.9)).cut(
 cq.Solid.makeCone(45.1,43,3.1,cq.Vector(0,0,31.9)))
housing=housing.fuse(transition_wall).fuse(male.translate((0,0,35))).clean()
# Flat central cover retains the exact existing roof's LED mounting bores.
deck=bounded_intersection(original_parts['base'],cyl(42.7,3,32)).translate((0,0,-32)).clean()
centers=[]
for i in range(3):
    a=2*math.pi*i/3
    x,y=37*math.cos(a),37*math.sin(a)
    centers.append((x,y))
    # Floor-grown supports; root broadens on floor, not into suspended ledges.
    housing=housing.fuse(cyl(5,32).translate((x,y,0))).fuse(
      cq.Solid.makeCone(7,5,2,cq.Vector(x,y,0))).clean()
    housing=housing.cut(cyl(1.85,4.6,27.5).translate((x,y,0))).cut(
      cq.Solid.makeCone(1.85,2.15,.3,cq.Vector(x,y,31.7))).clean()
    deck=deck.cut(cyl(1.7,3.2,-.1).translate((x,y,0))).cut(
      cq.Solid.makeCone(1.7,2,.3,cq.Vector(x,y,2.7))).clean()
    # Separate floor-grown locating posts: inward tangent r43, cover r42.7.
    lx,ly=44.5*math.cos(a),44.5*math.sin(a)
    housing=housing.fuse(cyl(1.5,35).translate((lx,ly,0))).clean()
for f in base_spec.features:
    if f.id in ('power_opening','button_opening'):
        housing=housing.cut(primitive(f,values)).clean()
# Finger/pry recesses cut into cover edge, no outward tabs.
for y in (-42.7,42.7):
    deck=deck.cut(cyl(4,4,-.5).translate((0,y,0))).clean()
for x,r in ((0,3.3),(26,1.7),(-26,1.7)):
    deck=deck.cut(cq.Solid.makeCone(r,r+.25,.25,cq.Vector(x,0,2.75))).clean()
# Entire vertical swept bounding cylinder is free from seating plane upwards.
sweep_overlap=bounded_intersection(housing,cyl(42.7,30,32.001)).Volume()
assert sweep_overlap<.001, 'Cover vertical removal obstructed'
assert deck.cut(cyl(42.70001,4,-.1)).Volume()<.001
assert 43-42.7>=.29999
tool_overlaps=[]
for x,y in centers:
    tool_overlaps.append(bounded_intersection(housing,cyl(3,25,32.001).translate((x,y,0))).Volume())
assert max(tool_overlaps)<.001, 'Insert/screw tool approach blocked'
# Collar is exactly preserved and connected through continuous tapered wall.
assert housing.isValid() and len(housing.Solids())==1
assert bounded_intersection(housing,cyl(43,6,35)).Volume()<.001
assert cyl(47.5,2.4,-2.4).cut(housing).Volume()<.001
deck_assembled=deck.translate((0,0,32))
collision=bounded_intersection(housing,deck_assembled).Volume()
assert collision<.01, 'Deck/housing collision'
# Closed floor and unobstructed central top insertion path.
floor_probe=cyl(44,2.4,-2.4)
assert floor_probe.cut(housing).Volume()<.001, 'Floor discontinuity'
assert bounded_intersection(housing,cyl(30,35,.01)).Volume()<.001, 'Top access blocked'
# Exact collar equality above roof; no thread geometry modified.
old_collar=bounded_intersection(original_parts['base'],cyl(50,6,35))
new_collar=bounded_intersection(housing,cyl(50,6,35))
assert old_collar.cut(new_collar).Volume()<.001
assert new_collar.cut(old_collar).Volume()<.001
# Export both revised parts floor/underside down. Assembly transforms recorded below.
parts['base']=housing.translate((0,0,2.4)).clean()
assert parts['base'].BoundingBox().xlen<=95.001
assert parts['base'].BoundingBox().ylen<=95.001
assert bounded_intersection(housing,cyl(30,41,.001)).Volume()<.001, 'Unexpected cavity fill'
parts['bottom_cover']=deck
for k in ('diffuser','led_core'):
    assert parts[k] is original_parts[k], 'Unrelated geometry replaced'
redesign_checks={
 'reference':{'url':'https://www.alpaco.it/generators/case/','author':'alpaco.it',
 'lesson':'Open-side-up housing and separate lid orientation only; no geometry copied; maker claims are not lamp print validation'},
 'part_roles':{'base':'closed-floor housing with integral exact male collar','bottom_cover':'flat central lift-out access cover'},
 'collar_aperture_mm':86.0,'cover_diameter_mm':85.4,'cover_thickness_mm':3,
 'cover_max_radius_mm':42.7,'vertical_swept_overlap_mm3':sweep_overlap,
 'tool_approach_overlap_mm3':tool_overlaps,
 'collar_support':'continuous tapered wall; 55.9 degree inner underside from horizontal; no horizontal annular roof',
 'remaining_support_limits':'Original thread flank radial projection 1.0 mm, slope about 45 degrees; crest flat 0.6 mm; side openings 13 and 7.2 mm geometric widths. Slicer bridge directions NOT_RUN',
 'removal_order':'Unscrew diffuser, disconnect LED wiring as necessary, remove three accessible M3 cover screws, lift cover and attached core vertically through collar. Reverse for assembly; core may be preattached to cover. Base remains one print.',
 'unchanged_geometry_comparison':{k:parts[k].cut(original_parts[k]).Volume()+original_parts[k].cut(parts[k]).Volume() for k in ('diffuser','led_core')},
 'assembly_translation_mm':{'base':[0,0,0],'bottom_cover':[0,0,34.4],'diffuser':[0,0,37.4],'led_core':[0,0,37.4]},
 'envelope_correction':{'limit_xy_mm':95.001,'removed_mm3':envelope_removed,
 'bounded_boolean':'PASSED','no_added_cavity_material':'PASSED',
 'internal_reinforcement_preserved':'PASSED'},
 'floor_mm':2.4,'housing_height_mm':43.4,'deck_height_mm':3,
 'locating_radial_clearance_mm':.3,'locating_overlap_mm':3,
 'insert_pocket_diameter_mm':3.7,'insert_pocket_depth_mm':4.5,
 'insert_nominal':'M3 brass OD4 x L4, flush upward entry; provisional pocket, coupon required',
 'screw':'3 x M3x6 socket head; 3 mm deck stack, 3 mm insert engagement, 1 mm to insert bottom; no washer assumed; verify actual hardware',
 'boss_root_underside_angle_from_horizontal_deg':45,
 'boss_construction':'floor-grown full-height posts, no suspended ledges',
 'side_opening_nominal_bridge_spans_mm':{'power':13,'button_max_width':7.2},
 'bridge_note':'Geometric opening widths only; actual extrusion direction and bridge quality NOT_RUN',
 'deck_housing_overlap_mm3':collision,'floor_continuity':'PASSED','central_top_access':'PASSED',
 'exact_transferred_collar':'PASSED','diffuser_core_identity':'unchanged shape objects',
 'slicer':'NOT_RUN','physical_fit':'NOT_RUN','electronics':'E1 untouched; no electronics operations',
 'print_orientation':{'base':'closed floor down, cavity up','bottom_cover':'flat underside directly on bed; no skirt or collar'},
 'old_volumes_mm3':old_volumes,
 'new_volumes_mm3':{k:s.Volume() for k,s in parts.items()},
 'dimensions_mm':{k:[s.BoundingBox().xlen,s.BoundingBox().ylen,s.BoundingBox().zlen] for k,s in parts.items()}
}
print('TOP_ACCESS_CHECKS',json.dumps(redesign_checks))
(ROOT/'top_access_checks.json').write_text(json.dumps(redesign_checks,indent=2))
counts={}
for key in ('base','diffuser'):
    counts[key]=sum(f.geomType()=='BSPLINE' for f in parts[key].Faces())
    assert counts[key]>0, 'Missing helical BSPLINE faces '+key
checks=[]
for t in (0,.25,.5,1,1.5):
    mating=female.rotate((0,0,0),(0,0,1),360*t).translate((0,0,35+pitch*t))
    overlap=bounded_intersection(housing,mating).Volume()
    assert bounded_intersection(deck_assembled,mating).Volume()<.01, 'Cover/diffuser interference'
    assert bounded_intersection(housing,mating).Volume()<.01, 'Housing/diffuser interference'
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
