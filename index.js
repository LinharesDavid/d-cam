const dotenv = require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const app = express()
const exec = require('child_process').exec; 
const ngrok = require('ngrok');
const crypto = require('crypto');
const fs = require('fs');

const iv = process.env.IV
const secret = process.env.KEY

let ngrok_url = null;

ngrok.authtoken(process.env.NGROK_TOKEN);

app.use(bodyParser.json());

app.get('/url', function (req, res) {
   let state = Number(getFileContent('./status.cam'));

    if (state == "0") {
        return res.send({"url": "", "state": state}); 
    }

    getRoute('http', 8081)
	.then(url => {
	    const cipher = crypto.createCipheriv('aes-256-cbc',	Buffer.from(secret), Buffer.from(iv));

	    let encrypted = cipher.update(Buffer.from(url), 'utf8', 'hex');
	    encrypted += cipher.final('hex');

	    return res.send({'url': encrypted, "state": state});
	})
        .catch(err => console.log(err));
});

app.post('/move', (req, res) => {
    let direction = req.body.direction

    exec(`python cam_position.py ${direction}`);  

    res.sendStatus(200);
});


app.post('/start', (req, res) => {
    exec(`./status.sh start`);

    res.sendStatus(200);
});

app.post('/stop', (req, res) => {
    exec('./status.sh stop', (err, stdout, stderr) => {
        if (err) {
           console.error(`exec error: ${err}`);
           return;
        }

        console.log(`Number of files ${stdout}`);
    });

    res.sendStatus(200);
});

app.get('/state', (req, res) => res.send(getFileContent('./status.cam')));

app.listen((process.env.PORT), function () {
    console.log(`App listenning on port ${process.env.PORT}`);
})

async function getRoute(protocol, port) {
    if (ngrok_url != null) {
        ngrok_url = await ngrok.disconnect();
    }

    ngrok_url = await ngrok.connect({proto: 'http', addr: port});
    return ngrok_url;
}

function getFileContent(path) {
    return fs.readFileSync(path, 'utf8');
}

