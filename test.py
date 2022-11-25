#!/usr/bin/env python3

from json import load as jsonload, loads as jsonloadstr
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl


def get_config(file_location):
  with open(file_location) as file:
    cfg = jsonload(file)
  return [cfg[k] for k in ('bot_token', 'chat_id', "hook_token")]

bot_token, chat_id, hook_token = get_config('./config.json')
hook_token_key = 'X-Telegram-Bot-Api-Secret-Token'


def get_example():
  url = "https://jsonplaceholder.typicode.com/posts/1"
  httprequest = Request(url, headers={"Accept": "application/json"})
  with urlopen(httprequest) as response:
    print(response.status)
    print(response.read().decode())





def tg_send_post_example():
  url = f'https://api.telegram.org/bot{token}/sendMessage'
  data = {"chat_id": chat_id, "text": "easy"}
  postdata = urlencode(data).encode()
  httprequest = Request(url, data=postdata, method="POST")
  with urlopen(httprequest) as response:
    print(response.read().decode())

class Server(BaseHTTPRequestHandler):
  def send404(self):
    content_bytes = bytes("Not Found\n", 'UTF-8')
    self.send_response(404)
    self.send_header('content-type', "text/plain")
    self.send_header('content-length', len(content_bytes))
    self.end_headers()
    self.wfile.write(content_bytes)

  def do_CONNECT(self):
    self.send404()
    
  def do_DELETE(self):
    self.send404()
    
  def do_GET(self):
    self.send404()
    
  def do_HEAD(self):
    self.send404()
    
  def do_OPTIONS(self):
    self.send404()
    
  def do_PUT(self):
    self.send404()
    
  def do_TRACE(self):
    self.send404()
    
  def do_POST(self):
    if ( (self.path == '/hook') and
         ('Content-Length' in self.headers) and
         ((hook_token_key in self.headers) and (self.headers[hook_token_key] == hook_token))
       ):
      #print(self.headers)
      content_length = int(self.headers['Content-Length'])
      post_data = jsonloadstr(self.rfile.read(content_length).decode("utf-8"))
      self.send_response(200)
      print(post_data)
    else:
      self.send404()

    
httpd = HTTPServer(('localhost', 8443), Server)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.check_hostname = False
ctx.load_cert_chain(certfile='public.pem', keyfile="private.key")
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
try:
  httpd.serve_forever()
except KeyboardInterrupt:
  pass
httpd.server_close()
