import pathlib,re,urllib.request,urllib.error,json,sys
root=pathlib.Path('/workspace/work/phase2-rm')
s=(root/'curso-arm.html').read_text()
url=re.search(r'https://[^\s\"\'<>]+\.r2\.dev',s).group()
request=urllib.request.Request(url+'/',method='HEAD')
try:
 with urllib.request.urlopen(request,timeout=15) as r: print(json.dumps({'url':url,'status':r.status,'scope':'HEAD host only, no asset certification'}))
except (urllib.error.URLError,TimeoutError) as e:
 print(json.dumps({'url':url,'status':'blocked','error':str(e),'scope':'No retry or alternate route attempted'}));sys.exit(3)
