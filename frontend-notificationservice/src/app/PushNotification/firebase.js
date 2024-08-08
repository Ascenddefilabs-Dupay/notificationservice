import { initializeApp } from 'firebase/app';
import { getMessaging, getToken, onMessage } from 'firebase/messaging';
import axios from 'axios';

const firebaseConfig = {
  apiKey: "AIzaSyBRhTld78mzJUCnBkOvcOw-XLB37tN8g7I",
  authDomain: "registration-database-c2085.firebaseapp.com",
  projectId: "registration-database-c2085",
  storageBucket: "registration-database-c2085.appspot.com",
  messagingSenderId: "767833958738",
  appId: "1:767833958738:web:e32fdd413dfc58f982f28b"
};

let messaging;

if (typeof window !== "undefined" && typeof navigator !== "undefined") {
  const app = initializeApp(firebaseConfig);
  messaging = getMessaging(app);

  navigator.serviceWorker.register('/firebase-messaging-sw.js')
    .then((registration) => {
      console.log('Service Worker registered with scope:', registration.scope);
      messaging = getMessaging(app, { serviceWorkerRegistration: registration });
    })
    .catch((error) => {
      console.error('Service Worker registration failed:', error);
    });
}

export const requestNotificationPermission = async () => {
  try {
    if (typeof window !== "undefined" && typeof Notification !== "undefined" && messaging) {
      const permission = await Notification.requestPermission();
      if (permission === 'granted') {
        const token = await getToken(messaging, { vapidKey: 'BE5G7DZIfeeWpLQkgvsKjzF5OPZlbaZwKGHEOvPLe5ktkX7O1gsxNUO-fnRlPw3bzI3JaqaL1RRG6ZGIKIZqW2I' });
        console.log('Token:', token);
        sendTokenToServer(token);
      } else {
        console.warn('Notification permission not granted');
      }
    } else {
      console.warn("Notifications are not supported in this environment");
    }
  } catch (error) {
    console.error('Error getting permission:', error);
  }
};

const sendTokenToServer = async (token) => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/save-token/', {
      method: 'POST',  // Ensure this is 'POST'
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ token })
    });

    const data = await response.json();
    console.log('Token sent to server:', data);
  } catch (error) {
    console.error('Error sending token to server:', error);
  }
};

// const sendTokenToServer = async (token) => {
//   try {
//     const response = await axios.post('http://127.0.0.1:8000/api/save-token/', { token });
//     console.log('Token sent to server:', response.data);
//   } catch (error) {
//     console.error('Error sending token to server:', error);
//   }
// };

const getTokenAndSendToServer = async () => {
  if (typeof window !== "undefined" && messaging) {
    try {
      const currentToken = await getToken(messaging, { vapidKey: 'BE5G7DZIfeeWpLQkgvsKjzF5OPZlbaZwKGHEOvPLe5ktkX7O1gsxNUO-fnRlPw3bzI3JaqaL1RRG6ZGIKIZqW2I' });
      if (currentToken) {
        console.log('Token:', currentToken);
        sendTokenToServer(currentToken);
      } else {
        console.log('No registration token available. Request permission to generate one.');
      }
    } catch (err) {
      console.error('An error occurred while retrieving token. ', err);
    }
  } else {
    console.warn("Messaging is not supported in this environment");
  }
};

getTokenAndSendToServer();

export const onMessageListener = () =>
  new Promise((resolve, reject) => {
    if (messaging) {
      onMessage(messaging, (payload) => {
        resolve(payload);
      });
    } else {
      reject(new Error("Messaging is not supported in this environment"));
    }
  });


// // src/app/PushNotification/firebase.js
// import { initializeApp } from 'firebase/app';
// import { getMessaging, getToken, onMessage } from 'firebase/messaging';
// import axios from 'axios';

// const firebaseConfig = {
//   apiKey: "AIzaSyBRhTld78mzJUCnBkOvcOw-XLB37tN8g7I",
//   authDomain: "registration-database-c2085.firebaseapp.com",
//   projectId: "registration-database-c2085",
//   storageBucket: "registration-database-c2085.appspot.com",
//   messagingSenderId: "767833958738",
//   appId: "1:767833958738:web:e32fdd413dfc58f982f28b"
// };

// const app = initializeApp(firebaseConfig);
// const messaging = getMessaging(app);

// export const requestNotificationPermission = async () => {
//   try {
//     await Notification.requestPermission();
//     const token = await getToken(messaging, { vapidKey: 'BE5G7DZIfeeWpLQkgvsKjzF5OPZlbaZwKGHEOvPLe5ktkX7O1gsxNUO-fnRlPw3bzI3JaqaL1RRG6ZGIKIZqW2I' });
//     console.log('Token:', token);
//     sendTokenToServer(token);
//   } catch (error) {
//     console.error('Error getting permission:', error);
//   }
// };

// const sendTokenToServer = async (token) => {
//   try {
//     await axios.post('/api/save-token/', { token });
//   } catch (error) {
//     console.error('Error sending token to server:', error);
//   }
// };

// export const onMessageListener = () =>
//   new Promise((resolve) => {
//     onMessage(messaging, (payload) => {
//       resolve(payload);
//     });
//   });

// // Example function to send notification
// export const sendNotification = async (token, title, body) => {
//   try {
//     await axios.post('/api/send-notification/', {
//       token,
//       title,
//       body
//     });
//   } catch (error) {
//     console.error('Error sending notification:', error);
//   }
// };
