import * as admin from "firebase-admin";
import { FieldValue } from "firebase-admin/firestore";
import * as express from 'express';
import * as cors from 'cors';

export const SubmitGroupTaskController = express();
SubmitGroupTaskController.use(cors({origin: true}));

SubmitGroupTaskController.post('/', async (req, res) => {
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
    res.status(400).send(errorMessage);
  }
});
