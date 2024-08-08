// public/firebase-messaging-sw.js
importScripts('https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.23.0/firebase-messaging-compat.js');

const firebaseConfig = {
  apiKey: "AIzaSyBRhTld78mzJUCnBkOvcOw-XLB37tN8g7I",
  authDomain: "registration-database-c2085.firebaseapp.com",
  projectId: "registration-database-c2085",
  storageBucket: "registration-database-c2085.appspot.com",
  messagingSenderId: "767833958738",
  appId: "1:767833958738:web:e32fdd413dfc58f982f28b"
};

firebase.initializeApp(firebaseConfig);

const messaging = firebase.messaging();

messaging.onBackgroundMessage(function(payload) {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
    icon: '/firebase-logo.png'
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});



// // public/firebase-messaging-sw.js
// importScripts('https://www.gstatic.com/firebasejs/9.0.0/firebase-app.js');
// importScripts('https://www.gstatic.com/firebasejs/9.0.0/firebase-messaging.js');

// firebase.initializeApp({
//   apiKey: "AIzaSyBRhTld78mzJUCnBkOvcOw-XLB37tN8g7I",
//   authDomain: "registration-database-c2085.firebaseapp.com",
//   projectId: "registration-database-c2085",
//   storageBucket: "registration-database-c2085.appspot.com",
//   messagingSenderId: "767833958738",
//   appId: "1:767833958738:web:e32fdd413dfc58f982f28b"
// });

// const messaging = firebase.messaging();

// messaging.onBackgroundMessage(function(payload) {
//   const notificationTitle = payload.notification.title;
//   const notificationOptions = {
//     body: payload.notification.body,
//     actions: payload.notification.actions,
//   };

//   self.registration.showNotification(notificationTitle, notificationOptions);
// });
