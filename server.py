import http.server
import socketserver
import os
import cgi
import random
import urllib.parse
import time

UPLOAD_DIR = 'uploads'
PORT = 8000

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Simple templates
CHECKLIST = """<form method='POST' enctype='multipart/form-data'>
<h3>課題チェックリスト</h3>
<label><input type='checkbox' name='chk1'> 要件1</label><br>
<label><input type='checkbox' name='chk2'> 要件2</label><br>
<label><input type='checkbox' name='chk3'> 要件3</label><br>
<input type='file' name='code'><br>
<input type='submit' value='submit'>
</form>"""

QUIZ = """<form method='POST' enctype='multipart/form-data'>
<h3>課題に関するクイズ: 2+2=?</h3>
<input type='text' name='answer'><br>
<input type='file' name='code'><br>
<input type='submit' value='submit'>
</form>"""

PEER_TEMPLATE = """<form method='POST' enctype='multipart/form-data'>
<h3>他の提出物を確認してください</h3>
{peer}
<textarea name='feedback' placeholder='feedback'></textarea><br>
<input type='file' name='code'><br>
<input type='submit' value='submit'>
</form>"""

VIEW_TEMPLATE = """<!DOCTYPE html><html><head><meta charset='utf-8'>
<script src='https://cdnjs.cloudflare.com/ajax/libs/processing.js/1.6.6/processing.min.js'></script></head><body>
<script type='application/processing' src='/uploads/{file}'></script>
<canvas></canvas>
</body></html>"""

INDEX = """<!DOCTYPE html><html><body>
<h2>Processing 提出システム</h2>
<ul>
<li><a href='/submit1'>チェックリストによる提出</a></li>
<li><a href='/submit2'>クイズによる提出</a></li>
<li><a href='/submit3'>相互評価による提出</a></li>
</ul>
</body></html>"""

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/submit1'):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(CHECKLIST.encode('utf-8'))
        elif self.path.startswith('/submit2'):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(QUIZ.encode('utf-8'))
        elif self.path.startswith('/submit3'):
            peer_html = self.random_peer_result()
            html = PEER_TEMPLATE.format(peer=peer_html)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        elif self.path.startswith('/view/'):
            fname = self.path[len('/view/'):]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(VIEW_TEMPLATE.format(file=fname).encode('utf-8'))
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(INDEX.encode('utf-8'))

    def do_POST(self):
        if self.path.startswith('/submit1'):
            self.save_submission()
        elif self.path.startswith('/submit2'):
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                                    environ={'REQUEST_METHOD':'POST'})
            if form.getvalue('answer') == '4':
                self.save_submission(form=form)
            else:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'Incorrect answer')
        elif self.path.startswith('/submit3'):
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                                    environ={'REQUEST_METHOD':'POST'})
            feedback = form.getvalue('feedback')
            if feedback:
                self.save_submission(form=form)
            else:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'Feedback required')
        else:
            self.send_error(404)

    def save_submission(self, form=None):
        if form is None:
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                                    environ={'REQUEST_METHOD':'POST'})
        fileitem = form['code'] if 'code' in form else None
        if fileitem is not None and fileitem.filename:
            fname = f"{int(time.time()*1000)}_{os.path.basename(fileitem.filename)}"
            path = os.path.join(UPLOAD_DIR, fname)
            with open(path, "wb") as f:
                f.write(fileitem.file.read())
            self.send_response(303)
            self.send_header('Location', f'/view/{fname}')
            self.end_headers()
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'No file uploaded')

    def random_peer_result(self):
        files = os.listdir(UPLOAD_DIR)
        if not files:
            return '<p>まだ提出物がありません</p>'
        fname = random.choice(files)
        return f"<p>他者の提出物: <a href='/view/{fname}' target='_blank'>{fname}</a></p>"

with socketserver.TCPServer(('', PORT), Handler) as httpd:
    print('Serving on port', PORT)
    httpd.serve_forever()
