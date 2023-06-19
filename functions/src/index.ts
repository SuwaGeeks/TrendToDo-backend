import * as functions from "firebase-functions";
import * as admin from "firebase-admin";
admin.initializeApp();

// ライフチェック用のエンドポイント
exports.helloWorld = functions.https.onRequest((req, res) => {
  res.send("Hello Firebase!");
});
