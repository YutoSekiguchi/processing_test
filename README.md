# Processing Submission Service

This project provides a simple Node.js web server for uploading and viewing Processing (`.pde`) sketches. The UI uses [Processing.js](https://processingjs.org/) from a CDN to run sketches in the browser.

## Running the server

Install dependencies and start the server:

```bash
npm install
npm start
```

The server listens on port `8000` by default. Open `http://localhost:8000` in your browser.

## Submission methods

- `/submit1` – displays a checklist of assignment requirements. Upload your `.pde` file after confirming the checklist.
- `/submit2` – asks a simple quiz about the assignment. Correctly answering allows the file to be submitted.
- `/submit3` – shows a random existing submission so you can send feedback before submitting your own file.

Uploaded files are stored in the `uploads` directory. After a successful upload you are redirected to `/view/<filename>` where your sketch is executed in the browser via Processing.js.

