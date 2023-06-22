import * as functions from "firebase-functions";
import * as admin from "firebase-admin";
import { FieldValue } from "firebase-admin/firestore";

export const SubmitUserTaskController = async (req: functions.https.Request, res: functions.Response<any>) => {
  res.set('Access-Control-Allow-Headers', '*');
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS, POST');
  
  // エラーのチェック
  var errorFlag = 200;

  // タスクIDとユーザIDの整合性を確認する
  if(req.body.taskId) {
    await admin.firestore().collection('userTasks').doc(req.body.taskId).get()
      .then((result) => {
        if(!result.exists) errorFlag = 404
        else {
          if(result.get('hostUserId') != req.body.userId) errorFlag = 401;
        }
      }).catch(err => {
        errorFlag = 404;
      })
  } else {
    errorFlag = 404;
  }

  if(errorFlag == 200) {
    // 達成するタスクのドキュメントの参照を取得
    const userTaskDoc = admin.firestore().collection('userTasks').doc(req.body.taskId);

    // 達成を記録
    await userTaskDoc.update({
      finishedAt: FieldValue.serverTimestamp()
    });

    // 変更後のタスクを取得
    const userTask = (await userTaskDoc.get()).data();

    res.json(userTask);
  } else {
    if(errorFlag == 401) res.status(401).send('ユーザIDが一致しません');
    else if(errorFlag == 404) res.status(404).send('指定したタスクIDのタスクが存在しません');
    else res.status(400).send('不明なエラーです');
  }
}