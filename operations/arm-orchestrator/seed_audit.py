"""Seed a NEW local ledger from reviewed evidence; refuses to overwrite."""
import json
from pathlib import Path
from arm import Orchestrator
root=Path(__file__).resolve().parent
path=root/'arm.sqlite'
if path.exists():raise SystemExit('Ledger exists; refusing to overwrite')
o=Orchestrator(path)
versions={'rm-training':('design/study-preview-20261019','24a584cb520c9d8e4f4e51e0ee7b0e5d6f0fd312'),'modo-training-app':('feat/rutina-agustin-link','0bb492437d3f24d2b29c1ed608ffc8080b21230a'),'calculadora-nutricion-deportiva':('feat/nutrisport-pro-local-mvp','e852644c4ce29635024eedbbf3fb8acfc6ff8df8')}
for item in json.loads((root/'backlog.json').read_text()):
 branch,sha=versions[item['project']]
 o.task(item['project'],item['id']+' '+item['title'],item['priority'],'draft_patch',branch,sha,item)
for project,title,file,status in [
 ('rm-training','Unitarias 7/7','rm-unit.log','passed'),
 ('rm-training','Flujos de estudio: 32 comprobaciones','rm-browser.log','passed'),
 ('rm-training','Preview: textos corruptos detectados','rm-preview.json','failed'),
 ('modo-training-app','Cuatro fallos funcionales reproducidos','modo-repro.json','failed'),
 ('calculadora-nutricion-deportiva','Unitarias 88/88','nutri-unit.log','passed'),
 ('calculadora-nutricion-deportiva','Build TypeScript y Vite','nutri-build.log','passed'),
 ('calculadora-nutricion-deportiva','E2E original 10/10','nutri-e2e.log','passed'),
 ('rm-training','Acceso a despliegues actuales','environment.json','blocked'),
 ('modo-training-app','Pruebas del núcleo ARM 20/20','orchestrator-tests.log','passed')]:
 branch,sha=versions[project];t=o.task(project,title,'P1','test',branch,sha,{'execution':'Completed in current Work session; imported evidence, not executed by this ledger','evidence':file});r=o.start(t);o.finish(r,status,root/'evidence'/file)
t=o.task('modo-training-app','Publicar paquete ARM en rama y preparar revisión','P1','push_branch','feat/arm-orchestrator-v1','ee3b6f5ca6865707bf3374722d51c1cad4c174ed',{'destination':'operations/arm-orchestrator/','scope':'Package only; no main, merge, production or paid actions','requires':'Explicit user approval before remote persistence'})
o.request_approval(t)
(root/'snapshot.json').write_text(json.dumps(o.export(),ensure_ascii=False,indent=2))
assert o.verify()
print(json.dumps({k:len(v) for k,v in o.export().items()}))
