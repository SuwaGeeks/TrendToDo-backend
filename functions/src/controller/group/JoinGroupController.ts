import * as functions from "firebase-functions";
import * as admin from "firebase-admin";
import { FieldValue } from "firebase-admin/firestore";

export const JoinGroupController = async (req: functions.https.Request, res: functions.Response<any>) => {
  var statusMsg = "";
  
  // リクエストボディの検証
  if(!req.body.groupId || !req.body.userId) statusMsg = "リクエストボディが不十分です。";

  // ユーザの確認
  if(req.body.userId) {
    await admin.firestore().collection('users').doc(req.body.userId).get()
      .then(result => {
        if(!result.exists) statusMsg = "指定したユーザが存在しません。";
      }).catch(err => {
        statusMsg = "指定したユーザが存在しません。";
      })
  }

  // グループの確認
  var targetGroup: any;
  if(req.body.groupId) {
    await admin.firestore().collection('groups').doc(req.body.groupId).get()
      .then(result => {
        if(!result.exists) statusMsg = "指定したグループが存在しません。";
        else targetGroup = result.data();
      }).catch(err => {
        statusMsg = "指定したグループが存在しません。";
      })
  }

  // グループに参加する
  if(statusMsg == "") {
    await admin.firestore().collection('groupUsers').add({
      userId: req.body.userId,
      groupId: req.body.groupId,
      joinedAt: FieldValue.serverTimestamp(),
      groupName: targetGroup.groupName,
    }).catch(err => {
      statusMsg = "グループに参加できませんでした。";
    })
  }

  if(statusMsg == "") res.json({joinedGroup: targetGroup});
  else res.status(400).send(statusMsg);
}