const functions = require('firebase-functions');
const express = require('express');
const app = express();
const fs = require('fs');

var { PythonShell } = require('python-shell');
const admin = require('firebase-admin');
const serviceAccount = require('./pastube-9b354-firebase-adminsdk-zlqt2-074303df31.json');
admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: "https://pastube-9b354.firebaseio.com"
});

let db = admin.firestore();

app.set('view engine', 'ejs');
app.engine('ejs', require('ejs').__express);

app.get('/', (req, res) => {
    db.collection('channels').get()
        .then((snapshot) => {
            res.render('index', { channels: snapshot, firebaseConfig: serviceAccount });
        })
        .catch((err) => {
            console.log('Error getting documents', err);
        });
    //response.render('index');
});

app.get('/channel/:channelId', (req, res) => {

    db.collection('channels').doc(req.params.channelId).collection('videos').orderBy('publishedAt', 'desc').get()
        .then(collections => {
            res.render('channel', { videos: collections });
        });

});

app.get('/video/:videoId', (req, res) => {
    res.render('video', { videoId: req.params.videoId });
});

app.post('/register/channel', (req, res) => {

    const channelId = req.body['channelId'];
    const getChannelPython = new PythonShell('./python/get_channel.py');
    getChannelPython.send(channelId);
    getChannelPython.on('message', function (channelOrigin) {
        const channel = JSON.parse(channelOrigin);

        db.collection('channels').doc(channelId).set({
            channelName: channel['items'][0]['snippet']['title'],
            publishedAt: new Date(channel['items'][0]['snippet']['publishedAt']),
            defaultThumbnail: channel['items'][0]['snippet']['thumbnails']['default']['url'],
            mediumThumbnail: channel['items'][0]['snippet']['thumbnails']['medium']['url'],
            highThumbnail: channel['items'][0]['snippet']['thumbnails']['high']['url']
        });

        const getVideosPython = new PythonShell('./python/get_videos.py');
        getVideosPython.send(channelId);
        getVideosPython.on('message', function (videosOrigin) {
            const videos = JSON.parse(videosOrigin);
            for (let video of videos['items']) {
                const videoId = video['id']['videoId'];
                db.collection('channels').doc(channelId).collection('videos').doc(videoId).set({
                    title: video['snippet']['title'],
                    publishedAt: new Date(video['snippet']['publishedAt']),
                    defaultThumbnail: video['snippet']['thumbnails']['default']['url'],
                    mediumThumbnail: video['snippet']['thumbnails']['medium']['url'],
                    highThumbnail: video['snippet']['thumbnails']['high']['url'],
                    //standardThumbnail: video['snippet']['thumbnails']['standard']['url'],
                    //maxresThumbnail: video['snippet']['thumbnails']['maxres']['url']
                });
            }
        });

        res.redirect('/');
    });
})

exports.app = functions.https.onRequest(app);
