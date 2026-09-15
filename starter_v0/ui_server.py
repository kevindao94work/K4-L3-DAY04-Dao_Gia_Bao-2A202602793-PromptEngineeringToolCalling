"""Local-only Helpdesk UI. No extra web framework dependency."""
from __future__ import annotations
import argparse
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from chat_runtime import ChatSession, ROOT
from env_loader import load_lab_env

SESSIONS={}
LOCKS={}
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass # do not log user text or secrets
    def reply(self,code,data,content_type='application/json; charset=utf-8'):
        body=json.dumps(data,ensure_ascii=False).encode() if content_type.startswith('application/json') else data
        self.send_response(code);self.send_header('Content-Type',content_type)
        self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Content-Security-Policy',"default-src 'self'; style-src 'self'; script-src 'self'; connect-src 'self'; frame-ancestors 'none'")
        self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
    def do_GET(self):
        files={'/':('index.html','text/html; charset=utf-8'),'/app.js':('app.js','text/javascript; charset=utf-8'),'/style.css':('style.css','text/css; charset=utf-8')}
        if self.path not in files:return self.reply(404,{'error':'not_found'})
        name,mime=files[self.path];return self.reply(200,(ROOT/'ui'/name).read_bytes(),mime)
    def do_POST(self):
        # Only our same-origin JS client (or an explicit local test client) may mutate sessions.
        expected=f'http://127.0.0.1:{self.server.server_port}'
        if self.headers.get('Host')!=f'127.0.0.1:{self.server.server_port}' or self.headers.get('Origin')!=expected or self.headers.get('X-Helpdesk-UI')!='1':
            return self.reply(403,{'error':'invalid_origin'})
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<=20000:return self.reply(413,{'error':'request_too_large'})
            body=json.loads(self.rfile.read(length));action=self.path
            if action=='/api/new':
                session=ChatSession(model=self.server.model);SESSIONS[session.id]=session;LOCKS[session.id]=threading.Lock()
                return self.reply(200,session.state())
            session=SESSIONS.get(body.get('session_id'))
            if session is None:return self.reply(404,{'error':'session_not_found'})
            with LOCKS[session.id]:
                if action=='/api/send':
                    text=body.get('message','')
                    if not isinstance(text,str) or not text.strip() or len(text)>6000:return self.reply(400,{'error':'invalid_message'})
                    state=session.send(text.strip())
                elif action=='/api/confirm':state=session.confirm(body.get('confirmation_id'))
                elif action=='/api/cancel':state=session.cancel()
                else:return self.reply(404,{'error':'not_found'})
                return self.reply(200,state)
        except ValueError as exc:return self.reply(409,{'error':'stale_confirmation' if str(exc)=='stale_confirmation' else 'invalid_request'})
        except Exception:return self.reply(500,{'error':'internal_error'})

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8765);parser.add_argument('--model',default='gpt-4o-mini');args=parser.parse_args()
    load_lab_env(ROOT)
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler);server.model=args.model
    print(f'Helpdesk UI: http://127.0.0.1:{args.port} (openai / {args.model}; v3 + chat-ui-v2)',flush=True)
    server.serve_forever()
if __name__=='__main__':main()
