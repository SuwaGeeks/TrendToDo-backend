import * as functions from "firebase-functions"
import * as admin from "firebase-admin";

export const AddGroupTaskController = async (
  req: functions.https.Request,
  res: functions.Response<any>
) => {
  
  // エラーのチェック
  var errorMessage = "";

  // タスク名が入力されていない
  if (typeof req.body.taskName != "string") errorMessage = "タスク名が入力されていません";

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
        if(!flag) errorMessage = "ユーザがグループに属していません";
        if(result.empty) errorMessage = "ユーザが見つかりません";
      })
      .catch((err) => {
        errorMessage = "不明なエラーです";
      });
  } else {
    errorMessage = "ユーザーIDが指定されていません";
  }

  if (errorMessage == "") {
    // タスクデータのオブジェクトを作成
    const taskData: { [prop: string]: any } = {
      taskGroupID: req.body.groupId,
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

    res.json({task: taskData});
  } else {
    res.status(400).send(errorMessage);
  }
};
