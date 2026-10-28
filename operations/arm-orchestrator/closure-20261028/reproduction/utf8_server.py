import functools,http.server,sys
class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map={**http.server.SimpleHTTPRequestHandler.extensions_map,
                    '.html':'text/html; charset=utf-8',
                    '.js':'text/javascript; charset=utf-8',
                    '.css':'text/css; charset=utf-8'}
    def log_message(self,*args):pass
http.server.ThreadingHTTPServer(('127.0.0.1',int(sys.argv[1])),functools.partial(Handler,directory=sys.argv[2])).serve_forever()
