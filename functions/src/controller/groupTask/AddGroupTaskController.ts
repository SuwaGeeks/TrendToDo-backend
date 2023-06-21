import * as functions from "firebase-functions"
import * as admin from "firebase-admin";

export const AddGroupTaskController = async (
  req: functions.https.Request,
  res: functions.Response<any>
) => {
  
  // エラーのチェック
  var errorFlag = 200;

  // タスク名が入力されていない
  if (typeof req.body.taskName != "string") errorFlag = 400;

  // ユーザがグループにいない/一致しない
  if (req.body.addUserId) {
    await admin
      .firestore()
      .collection("groupUsers")
      .where("userId", "==", req.body.addUserId)
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
    // タスクデータのオブジェクトを作成
    const taskData: { [prop: string]: any } = {
      taskGroupID: req.body.taskGroupID,
      taskName: req.body.taskName,
      taskContent: req.body.taskContent || null,
      taskLimit: req.body.taskLimit || null,
    };

    // コレクションの参照を取得
    const groupTaskCollection = admin.firestore().collection("groupTasks");

    // タスクの情報を追加
    const addResult = await groupTaskCollection.add(taskData);

    // タスクIDを追加
    taskData.taskId = addResult.id;

    // レスポンスを作成
    taskData.taskWeight = 0;
    taskData.meanTime = 0;
    taskData.finished = false;

    res.json(taskData);
  } else {
    switch (errorFlag) {
      case 400:
        res.status(400).send("タスク名が入力されていません");
        break;
      case 401:
        res.status(401).send("ユーザがグループにいません/一致しません");
        break;
      case 404:
        res.status(404).send("指定したユーザが見つかりません");
        break;
    }
  }
};
