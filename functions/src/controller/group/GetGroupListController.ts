import * as functions from "firebase-functions";
import * as admin from "firebase-admin";

import { GroupModel } from "../../model/GroupModel";

export const GetGroupListController = async (req: functions.https.Request, res: functions.Response<any>) => {
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
}