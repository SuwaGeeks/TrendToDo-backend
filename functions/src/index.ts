import * as functions from "firebase-functions";
import * as admin from "firebase-admin";
import { AddNewUserController } from "./controller/AddNewUserController";
admin.initializeApp();

// ライフチェック用のエンドポイント
exports.helloWorld = functions.https.onRequest((req, res) => {
  res.send("Hello Firebase!");
});

// ユーザ作成時に呼ばれるエンドポイント
exports.addNewUser = functions.auth.user().onCreate( AddNewUserController )