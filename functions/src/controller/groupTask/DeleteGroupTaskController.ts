import * as functions from "firebase-functions";
import * as admin from "firebase-admin";

export const DeleteGroupTaskController = async (
  req: functions.https.Request,
  res: functions.Response<any>
) => {
  //エラーのチェック
  var errorFlag = 200;

  // タスクIDとグループIDとの整合性を確認する
  if(req.body.taskId) {
    await admin.firestore().collection('groupTasks').doc(req.body.taskId).get()
      .then((result) => {
        if(!result.exists) errorFlag = 404
        else {
          if(result.get('taskGroupID') != req.body.groupId) errorFlag = 401;
        }
      }).catch(err => {
        errorFlag = 404;
      })
  } else {
    errorFlag = 404;
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
        if(!flag) errorFlag = 401;
        if(result.empty) errorFlag = 404;
      })
      .catch((err) => {
        errorFlag = 401;
      });
  } else {
    errorFlag = 401;
  }

  if (errorFlag == 200) {
    // 削除するドキュメントの参照を取得
    const groupTaskDoc = admin.firestore().collection("groupTasks").doc(req.body.taskId);

    // タスクの情報を更新
    await groupTaskDoc.delete();

    res.status(200).send("タスクを削除しました");
  } else {
    switch (errorFlag) {
      case 401:
        res.status(401).send("ユーザIDが一致しません");
        break;
      case 404:
        res.status(404).send("指定したタスクIDのタスクが存在しません");
        break;
    }
  }
};
