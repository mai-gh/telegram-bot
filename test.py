#!/usr/bin/env python3

from json import load as jsonload
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl


def get_config(file_location):
  with open(file_location) as file:
    cfg = jsonload(file)
  return [cfg[k] for k in ('token', 'chatId')]

token, chat_id = get_config('./config.json')


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

routes = {
  '/': "Hello World\n",
  '/favicon.ico': "fav\n",
}

class Server(BaseHTTPRequestHandler):
  def do_HEAD(self):
    return
    
  def do_GET(self):
    self.respond()
    
  def do_POST(self):
    return
    
  def handle_http(self, status, content_type):
    if self.path in routes:
      status = 200
      content_type = "text/plain"
      response_body = routes[self.path]
    else:
      status = 404
      content_type = "text/plain"
      response_body = "404 Not Found"

    content_bytes = bytes(response_body, 'UTF-8')
    self.send_response(status)
    self.send_header('content-type', content_type)
    self.send_header('content-length', len(content_bytes))
    self.end_headers()
    return content_bytes
    
  def respond(self):
    content = self.handle_http(200, 'text/html')
    self.wfile.write(content)

# openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -subj "/" -keyout key.pem -out cert.pem
httpd = HTTPServer(('localhost', 4443), Server)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.check_hostname = False
ctx.load_cert_chain(certfile='cert.pem', keyfile="./key.pem")
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
try:
  httpd.serve_forever()
except KeyboardInterrupt:
  pass
httpd.server_close()
