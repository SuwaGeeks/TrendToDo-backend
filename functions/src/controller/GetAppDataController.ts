import * as admin from "firebase-admin";
import * as express from 'express';
import * as cors from 'cors';

export const GetAppDataController = express();
GetAppDataController.use(cors({origin: true}));

GetAppDataController.post('/', async (req, res) => {
  res.set('Access-Control-Allow-Headers', '*');
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS, POST');
  
  var errorMessage = "";

  if(!req.body.userId) {
    errorMessage = "ユーザIDが指定されていません";
  } else {
    await admin.firestore().collection('users').doc(req.body.userId).get()
      .then(result => {
        if(!result.exists) errorMessage = "ユーザIDが間違っています";
      }).catch(err => {
        errorMessage = "不明なエラーです";
      })
  }

  if(errorMessage == "") {
    var responseData: {[prop: string]: any} = {};
    responseData.userTasks = [];

    // ユーザタスクの一覧を取得
    await admin.firestore().collection('userTasks').where("hostUserId", "==", req.body.userId).get()
      .then(result => {
        var userTasks: any[] = [];
        result.forEach(elm => {
          userTasks.push(elm.data());
        })
        responseData.userTasks = userTasks;
      })
    
    // ユーザの参加しているグループの一覧を取得する
    var groupInfos: {[prop: string]: any} = {}, groupIds: any[] = [], groupTasks: {[prop: string]: any} = {}, groupTasksFromTaskId: {[prop: string]: any} = {};
    await admin.firestore().collection('groupUsers').where("userId", "==", req.body.userId).get()
      .then(result => {
        result.forEach(elm => {
          groupIds.push(elm.get('groupId'));
          groupTasks[elm.get('groupId')] = [];
          groupInfos[elm.get('groupId')] = {
            groupId: elm.get('groupId'),
            groupName: elm.get('groupName'),
          };
        })
      })

    // ユーザの参加しているグループのタスクを取得する
    var groupTaskIds: any[] = [], groupTaskLogs: {[prop: string]: any} = {};
    await admin.firestore().collection('groupTasks').where("taskGroupID", "in", groupIds).get()
      .then(result => {
        result.forEach(elm => {
          groupTaskIds.push(elm.id)
          groupTaskLogs[elm.id] = [];
          groupTasksFromTaskId[elm.id] = elm.data();
        })
      })
    
    // グループタスクのログを取得する
    await admin.firestore().collection('groupTaskLogs').where("taskId", "in", groupTaskIds).get()
      .then(result => {
        result.forEach(elm => {
          groupTaskLogs[elm.get('taskId')].push(elm.data());
        })
      })

    // タスクの評価と平均時間を計算する
    for (const taskId of Object.keys(groupTaskLogs)) {
      // グループタスクの評価と実施時間の平均を計算する
      var timeCount = 0, evaCount = 0;
      var meanTime = 0, meanEva = 0;
      var finishedFlag = false;
      groupTaskLogs[taskId].forEach((elm: any) => {
        if(elm.userId == req.body.userId) finishedFlag = true;

        if(elm.eva) {
          evaCount++;
          meanEva += elm.eva;
        }
        if(elm.time) {
          timeCount++;
          meanTime += elm.time;
        }
      })
      if(evaCount != 0) meanEva /= evaCount;
      if(timeCount != 0) meanTime /= timeCount;
      groupTasksFromTaskId[taskId].taskWeight = meanEva;
      groupTasksFromTaskId[taskId].meanTime = meanTime;
      groupTasksFromTaskId[taskId].finished = finishedFlag;
      groupTasks[groupTasksFromTaskId[taskId]['taskGroupID']].push(groupTasksFromTaskId[taskId]);
    }

    // ユーザの所属しているグループの情報をまとめる
    var userGroups: any[] = [];
    groupIds.forEach(groupId => {
      var tempGroup: {[prop: string]: any} = {};
      tempGroup.groupInfo = groupInfos[groupId];
      tempGroup.groupTask = groupTasks[groupId];

      userGroups.push(tempGroup);
    })

    responseData.userGroups = userGroups;

    res.json(responseData);
  } else {
    res.status(404).send(errorMessage)
  }
})