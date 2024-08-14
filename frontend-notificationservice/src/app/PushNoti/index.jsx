'use client';
import React, { useEffect, useCallback, useState } from 'react';
import axios from 'axios';

const Index = () => {
  const [userId, setUserId] = useState('');

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
    if (!userId) {
      // alert('User ID is not set.');
      return;
    }

    axios.post('http://localhost:8000/api2/api2/create-notification/', {
      user_id: userId,
      email_id: 'user@example.com',
      message: 'This is your notification message!!',
      type: 'push notification',
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(response => {
        sendNotification(response.data.message); // Trigger the notification
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Failed to create notification');
      });
  };

  const requestNotificationPermission = useCallback(() => {
    if ('Notification' in window) {
      if (Notification.permission === 'default') {
        Notification.requestPermission().then(permission => {
          if (permission === 'granted') {
            createNotification();
          } else {
            alert('Notification permission is denied or ignored. Please enable notifications in your browser settings.');
          }
        });
      } else if (Notification.permission === 'granted') {
        createNotification();
      }
    }
  }, [userId]);

  useEffect(() => {
    axios.get('http://localhost:8000/api2/api2/get-user-id/')
      .then(response => {
        if (response.data.user_id) {
          setUserId(response.data.user_id);
        } else {
          alert('User ID is not set.');
        }
      })
      .catch(error => {
        console.error('Error fetching user ID:', error);
      });

    requestNotificationPermission();
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
//       user_id: 'dupA0001', // Replace with the actual user ID
//       email_id: 'user@example.com',
//       message: 'This is your notification message!!',
//       type: 'push notification', // Add the type field
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
