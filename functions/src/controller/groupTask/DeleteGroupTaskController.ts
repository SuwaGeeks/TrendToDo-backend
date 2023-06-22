import * as functions from "firebase-functions";
import * as admin from "firebase-admin";

export const DeleteGroupTaskController = async (
  req: functions.https.Request,
  res: functions.Response<any>
) => {
  res.set('Access-Control-Allow-Headers', '*');
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS, POST');
  
  // エラーのチェック
  var errorMessage = "";

  // タスクIDとグループIDとの整合性を確認する
  if(req.body.taskId) {
    await admin.firestore().collection('groupTasks').doc(req.body.taskId).get()
      .then((result) => {
        if(!result.exists) errorMessage = "指定したIDのタスクがありません"
        else {
          if(result.get('taskGroupID') != req.body.groupId) errorMessage = "タスクがグループにありません";
        }
      }).catch(err => {
        errorMessage = "不明なエラーです";
      })
  } else {
    errorMessage = "不明なエラーです";
  }

  // ユーザIDとグループIDとの整合性を確認する
  if (req.body.userId) {
    await admin
      .firestore()
      .collection("groupUsers")
      .where("userId", "==", req.body.userId)
      .get()
      .then((result) => {
        var flag = false;
        result.forEach(elm => {
          if(elm.get('groupId') == req.body.groupId) flag = true;
        })
        if(!flag) errorMessage = "ユーザがグループに居ません";
        if(result.empty) errorMessage = "ユーザが見つかりません";
      })
      .catch((err) => {
        errorMessage = "不明なエラーです";
      });
  } else {
    errorMessage = "不明なエラーです";
  }

  if (errorMessage == "") {
    // 削除するドキュメントの参照を取得
    const groupTaskDoc = admin.firestore().collection("groupTasks").doc(req.body.taskId);

    // タスクの情報を更新
    await groupTaskDoc.delete();

    res.status(200).send("タスクを削除しました");
  } else {
    res.status(400).send(errorMessage);
  }
};
