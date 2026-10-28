import pathlib,json,hashlib,sys
root=pathlib.Path('/workspace/work/phase2-arm/operations/arm-orchestrator')
snap=json.loads((root/'continuation-20261028/snapshot-continuation.json').read_text())
files=[p for p in root.rglob('*') if p.is_file() and '__pycache__' not in str(p)]
missing=[]
for r in snap['runs']:
 if not r.get('evidence'):continue
 evidence=json.loads(r['evidence'])
 matches=[p for p in files if p.name==evidence['file'] and hashlib.sha256(p.read_bytes()).hexdigest()==evidence['sha256']]
 if not matches:missing.append({'run':r['id'],'evidence':evidence})
prev='0'*64
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
for event in snap['events']:
 assert event['previous']==prev
 assert event['hash']==digest([event['at'],event['kind'],json.loads(event['data']),prev])
 prev=event['hash']
print(json.dumps({'runs_checked':len(snap['runs']),'events_checked':len(snap['events']),'chain_valid':True,'missing_evidence':missing},indent=2))
sys.exit(bool(missing))
