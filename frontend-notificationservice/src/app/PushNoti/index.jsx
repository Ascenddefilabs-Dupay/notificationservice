'use client';
import React, { useEffect, useCallback } from 'react';
import axios from 'axios';

const Index = () => {

  const sendNotification = (message) => {
    if ('Notification' in window && Notification.permission === 'granted') {
      const notification = new Notification('Dupay', {
        body: message,
        icon: './images/logo.png',
      });

      notification.addEventListener('click', () => {
        window.open('https://trello.com/b/gaKr5gi3/team-1', '_blank');
      });
    }
  };

  const createNotification = () => {
    axios.post('http://localhost:8000/api2/api2/create-notification/', {
      user_id: 'dupA0001', // Replace with the actual user ID
      email_id: 'user@example.com',
      message: 'This is your notification message!!',
      type: 'push notification', // Add the type field
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(response => {
        console.log('Notification ID:', response.data.notification_id);
        sendNotification(response.data.message); // Trigger the notification
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Failed to create notification');
      });
  };

  const requestNotificationPermission = useCallback(() => {
    if ('Notification' in window) {
      if (Notification.permission === 'default' || Notification.permission === 'denied') {
        Notification.requestPermission().then(function (permission) {
          if (permission === 'granted') {
            console.log('Notification permission granted!!');
            createNotification();
          } else {
            alert('Notification permission is denied or ignored. Please enable notifications in your browser settings.');
          }
        });
      } else if (Notification.permission === 'granted') {
        createNotification();
      }
    }
  }, []);

  useEffect(() => {
    if ('Notification' in window) {
      requestNotificationPermission();
    }
  }, [requestNotificationPermission]);

  return (
    <div>
      <main className="flex min-h-screen flex-col items-center justify-between p-24">
        <h1 className='text-4xl font-bold'>Hello</h1>
        <button
          onClick={createNotification}
          className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4'
        >
          Trigger Notification
        </button>
      </main>
    </div>
  );
};

export default Index;



// 'use client';
// import React, { useEffect, useCallback } from 'react';
// import axios from 'axios';

// const Index = () => {

//   const sendNotification = (message) => {
//     if ('Notification' in window && Notification.permission === 'granted') {
//       const notification = new Notification('Dupay', {
//         body: message,
//         icon: './images/logo.png',
//       });

//       notification.addEventListener('click', () => {
//         window.open('https://trello.com/b/gaKr5gi3/team-1', '_blank');
//       });
//     }
//   };

//   const createNotification = () => {
//     axios.post('http://localhost:8000/api2/api2/create-notification/', {
//       email: 'user@example.com',
//       message: 'This is your notification message!!',
//     }, {
//       headers: {
//         'Content-Type': 'application/json',
//       },
//     })
//       .then(response => {
//         console.log('Notification ID:', response.data.notification_id);
//         sendNotification(response.data.message); // Trigger the notification
//       })
//       .catch(error => {
//         console.error('Error:', error);
//         alert('Failed to create notification');
//       });
//   };

//   const requestNotificationPermission = useCallback(() => {
//     if ('Notification' in window) {
//       if (Notification.permission === 'default' || Notification.permission === 'denied') {
//         Notification.requestPermission().then(function (permission) {
//           if (permission === 'granted') {
//             console.log('Notification permission granted!!');
//             createNotification();
//           } else {
//             alert('Notification permission is denied or ignored. Please enable notifications in your browser settings.');
//           }
//         });
//       } else if (Notification.permission === 'granted') {
//         createNotification();
//       }
//     }
//   }, []);

//   useEffect(() => {
//     if ('Notification' in window) {
//       requestNotificationPermission();
//     }
//   }, [requestNotificationPermission]);

//   return (
//     <div>
//       <main className="flex min-h-screen flex-col items-center justify-between p-24">
//         <h1 className='text-4xl font-bold'>Hello</h1>
//         <button
//           onClick={createNotification}
//           className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4'
//         >
//           Trigger Notification
//         </button>
//       </main>
//     </div>
//   );
// };

// export default Index;
