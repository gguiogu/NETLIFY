import http.server
import socketserver
import os

class ErrorLogger(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/log_error':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            with open('error.log', 'a', encoding='utf-8') as f:
                f.write(post_data + '\n')
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    def log_message(self, format, *args):
        pass

PORT = 8080
with socketserver.TCPServer(("", PORT), ErrorLogger) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
