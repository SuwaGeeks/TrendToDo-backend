import * as express from 'express';
import * as cors from 'cors';
import { getAuth } from "firebase-admin/auth";

export const SessionLoginController = express();
SessionLoginController.use(cors({origin: true}));

SessionLoginController.post('/', async (req, res) => {
  res.set('Access-Control-Allow-Headers', '*');
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS, POST');

  const idToken = req.body.idToken.toString();

  const expiresIn = 60 * 60 * 24 * 5 * 1000;

  res.setHeader('Cache-Control', 'private');
  
  getAuth()
    .createSessionCookie(idToken, { expiresIn })
    .then(
      (sessionCookie) => {
        // Set cookie policy for session cookie.
        const options = { maxAge: expiresIn, httpOnly: true, secure: true };
        res.cookie('session', sessionCookie, options);
        res.end(JSON.stringify({ status: 'success' }));
      },
      (error) => {
        res.status(401).send('UNAUTHORIZED REQUEST!');
      }
    );
})