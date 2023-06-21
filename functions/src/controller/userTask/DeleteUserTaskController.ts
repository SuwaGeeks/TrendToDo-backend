import * as functions from "firebase-functions";
import * as admin from "firebase-admin";

export const DeleteUserTaskController = async (req: functions.https.Request, res: functions.Response<any>) => {
  // エラーのチェック
  var errorFlag = 200;

  // タスクIDとユーザIDの整合性を確認する
  if(req.body.taskId) {
    await admin.firestore().collection('userTasks').doc(req.body.taskId).get()
      .then((result) => {
        if(result.exists) errorFlag = 404
        else {
          if(result.get('ownerUserId') != req.body.userId) errorFlag = 401;
        }
      }).catch(err => {
        errorFlag = 404;
      })
  } else {
    errorFlag = 404;
  }

  if(errorFlag == 200) {
    // 削除するドキュメントの参照を取得
    const userTaskDoc = admin.firestore().collection('userTasks').doc(req.body.taskId);

    // タスクの情報を更新
    await userTaskDoc.delete();

    res.status(200).send("タスクを削除しました");
  } else {
    if(errorFlag == 401) res.status(401).send('ユーザIDが一致しません');
    else if(errorFlag == 404) res.status(404).send('指定したタスクIDのタスクが存在しません');
    else res.status(400).send('不明なエラーです');
  }
}