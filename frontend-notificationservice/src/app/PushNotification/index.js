// src/app/PushNotification/index.js
import { useEffect, useState } from 'react';
import { requestNotificationPermission, onMessageListener } from './firebase';

export default function PushNotification() {
  const [notification, setNotification] = useState({ title: '', body: '' });

  useEffect(() => {
    if (typeof window !== 'undefined') {
      onMessageListener()
        .then((payload) => {
          setNotification({
            title: payload.notification.title,
            body: payload.notification.body,
          });
        })
        .catch((err) => console.log('failed: ', err));
    }
  }, []);

  return (
    <div>
      <h1>Interactive Notifications</h1>
      <button onClick={requestNotificationPermission}>Enable Notifications</button>
      {notification.title && (
        <div>
          <h2>{notification.title}</h2>
          <p>{notification.body}</p>
        </div>
      )}
    </div>
  );
}



// // src/app/PushNotification/index.js
// import { useEffect, useState } from 'react';
// import { requestNotificationPermission, onMessageListener } from './firebase';

// export default function PushNotification() {
//   const [notification, setNotification] = useState({ title: '', body: '' });

//   useEffect(() => {
//     if (typeof window !== 'undefined') {
//       onMessageListener()
//         .then((payload) => {
//           setNotification({
//             title: payload.notification.title,
//             body: payload.notification.body,
//           });
//         })
//         .catch((err) => console.log('failed: ', err));
//     }
//   }, []);

//   return (
//     <div>
//       <h1>Interactive Notifications</h1>
//       <button onClick={requestNotificationPermission}>Enable Notifications</button>
//       {notification.title && (
//         <div>
//           <h2>{notification.title}</h2>
//           <p>{notification.body}</p>
//         </div>
//       )}
//     </div>
//   );
// }
