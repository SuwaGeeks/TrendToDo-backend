import * as admin from "firebase-admin";
import { GroupModel } from "../../model/GroupModel";
import * as express from 'express';
import * as cors from 'cors';

export const CreateGroupController = express();
CreateGroupController.use(cors({origin: true}));

CreateGroupController.post('/', async (req, res) => {
  res.set('Access-Control-Allow-Headers', '*');
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS, POST');
  
  var status = 200;

  // リクエスト内容の精査
  if(!req.body.groupName) status = 400;

  // 新しいグループの作成
  if(status == 200) {
    const groupsCollectionRef = admin.firestore().collection('groups');
    const addGroupResult = await groupsCollectionRef.add({groupName: req.body.groupName});
  
    // レスポンスデータの作成
    const createdGroup: GroupModel = {
      groupId: addGroupResult.id,
      groupName: req.body.groupName,
    }

    res.json({createdGroup: createdGroup});
  } else {
    if(status == 400) res.status(400).send("グループ名が入力されていません");
    else res.status(400).send("不明なエラーです");
  }

})
