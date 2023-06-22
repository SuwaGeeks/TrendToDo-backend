import * as admin from "firebase-admin";
import { FieldValue } from "firebase-admin/firestore";

export const AddNewUserController = (user: admin.auth.UserRecord) => {
  // コレクションの参照を取得
  const userCollectionRef = admin.firestore().collection('users');

  // ユーザテーブルにログインした人の情報を追加
  userCollectionRef.doc(user.uid).set({
    'email': user.email,
    'displayName': user.displayName,
    'creationTime': user.metadata.creationTime,
  })

  // グループに参加する
  admin.firestore().collection('groupUsers').add({
    userId: user.uid,
    groupId: "V1PZQENRlcTVqZfVdBCr",
    joinedAt: FieldValue.serverTimestamp(),
    groupName: "技育CAMP アドバンス",
  })

  return true;
}