const express = require('express');
const fileUpload = require('express-fileupload');
const fs = require('fs');
const path = require('path');

const UPLOAD_DIR = path.join(__dirname, 'uploads');
const PORT = process.env.PORT || 8000;

if (!fs.existsSync(UPLOAD_DIR)) {
  fs.mkdirSync(UPLOAD_DIR);
}

const app = express();
app.use(fileUpload());
app.use('/uploads', express.static(UPLOAD_DIR));

const head = `<!DOCTYPE html><html><head><meta charset="utf-8">
<script src="https://cdnjs.cloudflare.com/ajax/libs/processing.js/1.6.6/processing.min.js"></script></head><body>`;
const foot = '</body></html>';

function indexPage() {
  return `${head}<h2>Processing 提出システム</h2><ul>
    <li><a href="/submit1">チェックリストによる提出</a></li>
    <li><a href="/submit2">クイズによる提出</a></li>
    <li><a href="/submit3">相互評価による提出</a></li>
  </ul>${foot}`;
}

function checklistPage() {
  return `${head}<form method="POST" enctype="multipart/form-data">
    <h3>課題チェックリスト</h3>
    <label><input type="checkbox" name="chk1"> 要件1</label><br>
    <label><input type="checkbox" name="chk2"> 要件2</label><br>
    <label><input type="checkbox" name="chk3"> 要件3</label><br>
    <input type="file" name="code"><br>
    <button type="submit">submit</button>
  </form>${foot}`;
}

function quizPage() {
  return `${head}<form method="POST" enctype="multipart/form-data">
    <h3>課題に関するクイズ: 2+2=?</h3>
    <input type="text" name="answer"><br>
    <input type="file" name="code"><br>
    <button type="submit">submit</button>
  </form>${foot}`;
}

function peerPage(peerHtml) {
  return `${head}<form method="POST" enctype="multipart/form-data">
    <h3>他の提出物を確認してください</h3>
    ${peerHtml}
    <textarea name="feedback" placeholder="feedback"></textarea><br>
    <input type="file" name="code"><br>
    <button type="submit">submit</button>
  </form>${foot}`;
}

function viewPage(file) {
  return `${head}<script type="application/processing" src="/uploads/${file}"></script><canvas></canvas>${foot}`;
}

app.get('/', (req, res) => res.send(indexPage()));
app.get('/submit1', (req, res) => res.send(checklistPage()));
app.post('/submit1', (req, res) => saveSubmission(req, res));

app.get('/submit2', (req, res) => res.send(quizPage()));
app.post('/submit2', (req, res) => {
  if (req.body && req.body.answer === '4') {
    saveSubmission(req, res);
  } else {
    res.send('Incorrect answer');
  }
});

app.get('/submit3', (req, res) => {
  const files = fs.readdirSync(UPLOAD_DIR);
  let peerHtml = '<p>まだ提出物がありません</p>';
  if (files.length) {
    const fname = files[Math.floor(Math.random() * files.length)];
    peerHtml = `<p>他者の提出物: <a href="/view/${fname}" target="_blank">${fname}</a></p>`;
  }
  res.send(peerPage(peerHtml));
});

app.post('/submit3', (req, res) => {
  if (req.body && req.body.feedback) {
    saveSubmission(req, res);
  } else {
    res.send('Feedback required');
  }
});

app.get('/view/:file', (req, res) => {
  res.send(viewPage(req.params.file));
});

function saveSubmission(req, res) {
  if (!req.files || !req.files.code) {
    res.status(400).send('No file uploaded');
    return;
  }
  const file = req.files.code;
  const fname = Date.now() + '_' + path.basename(file.name);
  const dest = path.join(UPLOAD_DIR, fname);
  file.mv(dest, err => {
    if (err) {
      res.status(500).send('Upload error');
    } else {
      res.redirect('/view/' + fname);
    }
  });
}

app.listen(PORT, () => console.log('Server listening on', PORT));

