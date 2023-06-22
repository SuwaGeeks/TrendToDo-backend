import * as express from 'express';
import * as cors from 'cors';
import { getAuth } from "firebase-admin/auth";

export const SessionLogoutController = express();
SessionLogoutController.use(cors({origin: true}));

SessionLogoutController.post('/', async (req, res) => {
  res.set('Access-Control-Allow-Headers', '*');
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS, POST');

  const sessionCookie = req.cookies.session || '';
  res.clearCookie('session');
  getAuth()
    .verifySessionCookie(sessionCookie)
    .then((decodedClaims) => {
      return getAuth().revokeRefreshTokens(decodedClaims.sub);
    })
    .then(() => {
      res.redirect('/login');
    })
    .catch((error) => {
      res.redirect('/login');
    });
});