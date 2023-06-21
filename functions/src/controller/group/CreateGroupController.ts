import * as functions from "firebase-functions";
import * as admin from "firebase-admin";
import { GroupModel } from "../../model/GroupModel";

export const CreateGroupController = async (req: functions.https.Request, res: functions.Response<any>) => {
  var status = 200;

  // リクエスト内容の精査
  if(!req.body.groupName) status = 400;

  // 新しいグループの作成
  const groupsCollectionRef = admin.firestore().collection('groups');
  const addGroupResult = await groupsCollectionRef.add({groupName: req.body.groupName});

  // レスポンスデータの作成
  const createdGroup: GroupModel = {
    groupId: addGroupResult.id,
    groupName: req.body.groupName,
  }

  if(status == 400) res.status(400).send("グループ名が入力されていません");
  else if(status == 200) res.json({createdGroup: createdGroup});
  else res.status(400).send("不明なエラーです");
}
