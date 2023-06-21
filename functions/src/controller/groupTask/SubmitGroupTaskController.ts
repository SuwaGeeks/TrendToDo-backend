import * as functions from "firebase-functions";
import * as admin from "firebase-admin";
import { FieldValue } from "firebase-admin/firestore";

export const SubmitGroupTaskController = async (
  req: functions.https.Request,
  res: functions.Response<any>
) => {
  // エラーのチェック
  var errorFlag = 202;

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

  if (errorFlag == 202) {
    // 達成するタスクのドキュメントの参照を取得
    const groupTaskLogsDoc = admin
      .firestore()
      .collection("groupTaskLogs");

    // 達成を記録
    await groupTaskLogsDoc.add({
      taskId: req.body.taskId,
      userId: req.body.userId,
      finishedAt: FieldValue.serverTimestamp(),
      eva: req.body.evaluation || null,
      time: req.body.time || null,
    });

    // 対象のグループタスクを取得
    const groupTask = await admin
      .firestore()
      .collection('groupTasks')
      .doc(req.body.taskId)
      .get();
    
    // 対象のグループタスクのログを取得
    const groupTaskLogs = await admin
      .firestore()
      .collection('groupTaskLogs')
      .where("taskId", "==", req.body.taskId)
      .get();
    
    // グループタスクの評価と実施時間の平均を計算する
    var timeCount = 0, evaCount = 0;
    var meanTime = 0, meanEva = 0;
    groupTaskLogs.forEach(elm => {
      if(elm.get('eva')) {
        evaCount++;
        meanEva += elm.get('eva');
      }
      if(elm.get('time')) {
        timeCount++;
        meanTime += elm.get('time');
      }
    })
    if(evaCount != 0) meanEva /= evaCount;
    if(timeCount != 0) meanTime /= timeCount;

    // レスポンスを作成
    var responseData = groupTask.data();
    if(responseData) {
      responseData.taskId = req.body.taskId;
      responseData.taskWeight = meanEva;
      responseData.meanTime = meanTime;
      responseData.finished = true;
    }

    res.json({task: responseData});
  } else {
    switch (errorFlag) {
      case 401:
        res.status(401).send("ユーザIDがグループに参加していないか、グループが存在しません");
        break;
      case 404:
        res.status(404).send("指定したタスクIDのタスクが存在しません");
        break;
    }
  }
};
