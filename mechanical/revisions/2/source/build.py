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
for part_id,shape in parts.items():
    cq.exporters.export(shape,str(ROOT/(part_id+'.step')))
