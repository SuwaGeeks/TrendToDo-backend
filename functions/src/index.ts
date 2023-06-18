import * as functions from "firebase-functions";
import * as admin from "firebase-admin";
admin.initializeApp();

exports.helloWorld = functions.https.onRequest((request, response) => {
  response.send("Hello Firebase!");
});
