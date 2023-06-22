import * as functions from "firebase-functions";
import * as admin from "firebase-admin";
admin.initializeApp();

import { AddNewUserController } from "./controller/AddNewUserController";

import { GetAppDataController } from "./controller/GetAppDataController";
import { AddUserTaskController } from "./controller/userTask/AddUserTaskController";
import { UpdateUserTaskController } from "./controller/userTask/UpdateUserTaskController";
import { DeleteUserTaskController } from "./controller/userTask/DeleteUserTaskController";
import { SubmitUserTaskController } from "./controller/userTask/SubmitUserTaskController";

import { JoinGroupController } from "./controller/group/JoinGroupController";
import { CreateGroupController } from "./controller/group/CreateGroupController";
import { GetGroupListController } from "./controller/group/GetGroupListController";

import { AddGroupTaskController } from "./controller/groupTask/AddGroupTaskController";
import { UpdateGroupTaskController } from "./controller/groupTask/UpdateGroupTaskController";
import { DeleteGroupTaskController } from "./controller/groupTask/DeleteGroupTaskController";
import { SubmitGroupTaskController } from "./controller/groupTask/SubmitGroupTaskController";

// ライフチェック用のエンドポイント
exports.helloWorld = functions.https.onRequest((req, res) => {
  res.set('Access-Control-Allow-Headers', '*');
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS, POST');

  res.send("Hello Firebase!");
});

// ユーザ作成時に呼ばれるエンドポイント
exports.addNewUser = functions.auth.user().onCreate( AddNewUserController );

// アプリのデータを取得するエンドポイント
exports.getAppData = functions.https.onRequest( GetAppDataController );

// 新しい個人タスクを追加するエンドポイント
exports.addUserTask = functions.https.onRequest( AddUserTaskController );
// 指定した個人タスクの内容を変更するエンドポイント
exports.updateUserTask = functions.https.onRequest( UpdateUserTaskController );
// 指定した個人タスクを削除するエンドポイント
exports.deleteUserTask = functions.https.onRequest( DeleteUserTaskController );
// 指定した個人タスクを消化するエンドポイント
exports.submitUserTask = functions.https.onRequest( SubmitUserTaskController );

// 指定したグループに所属するエンドポイント
exports.joinGroup = functions.https.onRequest( JoinGroupController );
// 新しいグループを作成するエンドポイント
exports.createGroup = functions.https.onRequest( CreateGroupController );
// グループの一覧を取得するエンドポイント
exports.getGroupList = functions.https.onRequest( GetGroupListController );

// 新しいグループタスクを追加するエンドポイント
exports.addGroupTask = functions.https.onRequest( AddGroupTaskController );
// 指定したグループタスクの内容を変更するエンドポイント
exports.updateGroupTask = functions.https.onRequest( UpdateGroupTaskController );
// 指定したグループタスクを削除するエンドポイント
exports.deleteGroupTask = functions.https.onRequest( DeleteGroupTaskController );
// 指定したグループタスクを消化するエンドポイント
exports.submitGroupTask = functions.https.onRequest( SubmitGroupTaskController );

