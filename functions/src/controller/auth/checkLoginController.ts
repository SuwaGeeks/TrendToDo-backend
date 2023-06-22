import * as express from 'express';
import * as cors from 'cors';
import { getAuth } from "firebase-admin/auth";

export const CheckLoginController = express();
CheckLoginController.use(cors({origin: true}));

CheckLoginController.post('/', async (req, res) => {
  res.set('Access-Control-Allow-Headers', '*');
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS, POST');

  var sessionCookie = ""
  if(req.cookies) {
    sessionCookie = req.cookies.session || '';
  }
  
  getAuth()
    .verifySessionCookie(sessionCookie, true)
    .then((decodedClaims) => {
      res.status(200).json({userId: decodedClaims.uid});
    })
    .catch((error) => {
      res.status(404).send('ユーザが見つかりません')
    });
});