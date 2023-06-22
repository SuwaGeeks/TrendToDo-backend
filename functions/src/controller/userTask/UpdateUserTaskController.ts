import * as functions from "firebase-functions";
import * as admin from "firebase-admin";

export const UpdateUserTaskController = async (req: functions.https.Request, res: functions.Response<any>) => {
  // エラーのチェック
  var errorFlag = 200;

  // タスクIDとの整合性を確認する
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
    // 更新内容のオブジェクトを作成
    const updateData: {[prop: string]: any} = {};

    if(req.body.taskName) updateData.taskName = req.body.taskName;
    if(req.body.taskContent) updateData.taskContent = req.body.taskContent;
    if(req.body.taskLimit) updateData.taskLimit = req.body.taskLimit;

    // コレクションの参照を取得
    const userTaskDoc = admin.firestore().collection('userTasks').doc(req.body.taskId);

    // タスクの情報を更新
    await userTaskDoc.update(updateData);

    // 変更後のタスクを取得
    const userTask = (await userTaskDoc.get()).data();

    res.json(userTask);
  } else {
    if(errorFlag == 401) res.status(401).send('ユーザIDが一致しません');
    else if(errorFlag == 404) res.status(404).send('指定したタスクIDのタスクが存在しません');
    else res.status(400).send('不明なエラーです');
  }
}