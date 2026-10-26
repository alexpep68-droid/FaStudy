"""Serve the fixed private library on loopback only. No corpus is copied into Git."""
import argparse,hashlib,json,re
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlparse

def load_library(folder):
    records=json.loads((folder/'respaldo-verificado.json').read_text(encoding='utf-8-sig'))
    if len(records)!=72 or len({r['sha256'] for r in records})!=72:
        raise ValueError('Expected exactly 72 unique PDF hashes')
    docs=[];files={}
    for r in records:
        sha=r['sha256']
        if not re.fullmatch('[a-f0-9]{64}',sha):raise ValueError('Invalid hash')
        file=(folder/'pdf'/r['archivo']).resolve()
        if not file.is_relative_to((folder/'pdf').resolve()):raise ValueError('Invalid file path')
        if hashlib.sha256(file.read_bytes()).hexdigest()!=sha:raise ValueError('PDF hash mismatch')
        doc=json.loads((folder/'catalogos'/(sha+'.json')).read_text(encoding='utf-8'))['documents'][0]
        if doc['sha256']!=sha:raise ValueError('Catalog hash mismatch')
        doc['sourceUrl']='/library/pdf/'+sha+'.pdf'
        doc['pages']=[p for p in doc['pages'] if p['text'].strip()]
        docs.append(doc);files[sha]=file
    return {'version':1,'documents':docs},files

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--library',type=Path,required=True)
    parser.add_argument('--port',type=int,default=4175)
    args=parser.parse_args();catalog,files=load_library(args.library.resolve())
    data=json.dumps(catalog,ensure_ascii=False).encode()
    web=Path(__file__).resolve().parent.parent/'web'
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            route=urlparse(self.path).path
            if route=='/library/status.json':return self.send_data(b'{"available":true,"expectedDocuments":72}','application/json')
            if route=='/library/catalog.json':return self.send_data(data,'application/json; charset=utf-8')
            match=re.fullmatch(r'/library/pdf/([a-f0-9]{64})\.pdf',route)
            if match and match[1] in files:return self.send_data(files[match[1]].read_bytes(),'application/pdf')
            assets={'/':('index.html','text/html'),'/index.html':('index.html','text/html'),'/app.js':('app.js','text/javascript'),'/library.js':('library.js','text/javascript'),'/style.css':('style.css','text/css')}
            if route in assets:
                name,mime=assets[route];return self.send_data((web/name).read_bytes(),mime+'; charset=utf-8')
            self.send_error(404)
        def send_data(self,body,mime):
            self.send_response(200);self.send_header('Content-Type',mime)
            self.send_header('Content-Length',str(len(body)));self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(body)
        def log_message(self,*args):pass
    print(f'FaStudy: http://127.0.0.1:{args.port} — 72 PDF verified by SHA-256',flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()

if __name__=='__main__':main()
