import * as admin from "firebase-admin";

import { GroupModel } from "../../model/GroupModel";
import * as express from 'express';
import * as cors from 'cors';

export const GetGroupListController = express();
GetGroupListController.use(cors({origin: true}));

GetGroupListController.post('/', async (req, res) => {
  res.set('Access-Control-Allow-Headers', '*');
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS, POST');
  
  // 全てのグループを取得
  const groups = await admin.firestore().collection('groups').get();

  // グループ一覧を作成
  var responseData: any[] = [];
  groups.forEach(elm => {
    var group: GroupModel = {
      groupId: elm.id,
      groupName: elm.get('groupName')
    }
    responseData.push(group);
  })

  if(responseData.length != 0) {
    res.json({groups: responseData});
  } else {
    res.status(404).send('グループがありません');
  }
})