import * as functions from "firebase-functions";
import * as admin from "firebase-admin";

export const AddUserTaskController = async (req: functions.https.Request, res: functions.Response<any>) => {
  res.set('Access-Control-Allow-Headers', '*');
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS, POST');
  
  // エラーのチェック
  var errorFlag = 200;

  // タスク名が入力されていない
  if(typeof req.body.taskName != 'string') errorFlag = 400;

  // 指定したユーザIDが間違っている
  if(req.body.addUserId) {
    await admin.firestore().collection('users').doc(req.body.addUserId || "").get()
    .then((result) => {
      if(!result.exists) errorFlag = 404;
    }).catch(err => {
      errorFlag = 404;
    })
  } else {
    errorFlag = 404;
  }

  if(errorFlag == 200) {
    // タスクデータのオブジェクトを作成
    const taskData: {[prop: string]: any} = {
      'hostUserId': req.body.addUserId,
      'taskName': req.body.taskName,
      'taskContent': req.body.taskContent || null,
      'taskLimit': req.body.taskLimit || null,
      'finishedAt': null
    };

    // コレクションの参照を取得
    const userTaskCollection = admin.firestore().collection('userTasks');

    // タスクの情報を追加
    const addResult = await userTaskCollection.add(taskData);

    // タスクIDを追加
    taskData.taskId = addResult.id;

    res.json(taskData);
  } else {
    if(errorFlag == 400) res.status(400).send('タスク名が入力されていません');
    else if(errorFlag == 404) res.status(404).send('ユーザが見つかりません');
    else res.status(400).send('不明なエラーです');
  }
}