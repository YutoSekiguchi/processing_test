# Processing Submission Service

This sample project provides a simple HTTP server for submitting and viewing Processing (`.pde`) sketches using three different submission modes. The server relies only on Python standard libraries and serves a minimal HTML UI that uses [Processing.js](https://processingjs.org/) from a CDN to run uploaded sketches in the browser.

## Running the server

```bash
python3 server.py
```

The server listens on port `8000` by default. Open `http://localhost:8000` in your browser.

## Submission methods

- `/submit1` – displays a checklist of assignment requirements. Upload your `.pde` file after confirming the checklist.
- `/submit2` – asks a simple quiz about the assignment. Correctly answering allows the file to be submitted.
- `/submit3` – shows a random existing submission so you can send feedback before submitting your own file.

Uploaded files are stored in the `uploads` directory. After a successful upload you are redirected to `/view/<filename>` where your sketch is executed in the browser via Processing.js.
