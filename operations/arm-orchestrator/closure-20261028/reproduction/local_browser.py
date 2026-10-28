"""Run reviewed local browser scripts with a bounded loopback-only server."""
import argparse,os,pathlib,subprocess,sys,time,urllib.request
p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--port',required=True,type=int);p.add_argument('--raw',action='store_true');p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args()
cmd=a.command[1:] if a.command[0]=='--' else a.command
env=os.environ.copy();env['CHROME_PATH']='/usr/bin/chromium';env['CHROMIUM_PATH']='/usr/bin/chromium';env['PLAYWRIGHT_MODULE']='/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright';env['APP_URL']='http://127.0.0.1:'+str(a.port)
server_command=([sys.executable,'-m','http.server',str(a.port),'--bind','127.0.0.1','--directory',a.root] if a.raw else [sys.executable,'/workspace/work/utf8_server.py',str(a.port),a.root])
server=subprocess.Popen(server_command,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
 opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
 for i in range(50):
  if server.poll() is not None: raise RuntimeError('Local server exited')
  try:
   opener.open(env['APP_URL'],timeout=1).close();break
  except OSError:time.sleep(.1)
 else:raise RuntimeError('Local server not ready')
 r=subprocess.run(cmd,cwd=a.root,env=env,timeout=90)
 sys.exit(r.returncode)
finally:
 server.terminate()
 try:server.wait(timeout=5)
 except subprocess.TimeoutExpired:server.kill();server.wait()
