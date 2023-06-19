import * as admin from "firebase-admin";

export const AddNewUserController = (user: admin.auth.UserRecord) => {
  // コレクションの参照を取得
  const userRef = admin.firestore().collection('users');

  // ユーザテーブルにログインした人の情報を追加
  userRef.doc(user.uid).set({
    'email': user.email,
    'displayName': user.displayName,
    'creationTime': user.metadata.creationTime,
  })

  return true;
}