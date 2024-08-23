'use client';
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const AccountActivity = () => {
  const [userId, setUserId] = useState('');

  // Function to send a browser notification
  const sendNotification = (title, message, icon, link) => {
    if ('Notification' in window && Notification.permission === 'granted') {
      const notification = new Notification(title, {
        body: message,
        icon: icon,
      });

      // Handle notification click event
      notification.onclick = () => {
        window.open(link, '_blank');
      };
    }
  };

  // Function to request notification permission from the user
  const requestNotificationPermission = () => {
    if ('Notification' in window && Notification.permission !== 'granted') {
      Notification.requestPermission().then(permission => {
        if (permission !== 'granted') {
          alert('Notification permissions are not granted. Please enable them in your browser settings.');
        }
      });
    }
  };

  // Function to create and trigger the AccountActivity notification immediately
  const createImmediateNotification = () => {
    if (!userId) {
      alert("User ID is not available.");
      return;
    }

    axios.post('http://localhost:8000/api7/create-account-activity/', {
      email_id: 'user@example.com',
      message: 'This is an account activity just for you!',
      delay: '0',  // No delay for immediate notification
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(response => {
        // Display notification immediately
        const message = response.data.message || 'This is an account activity just for you!';
        sendNotification('Account Activity', message, './images/logo.png', 'https://www.google.com/');
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Failed to create account activity notification.');
      });
  };

  // Function to create and trigger the AccountActivity notification with a delay
  const createDelayedNotification = () => {
    if (!userId) {
      alert("User ID is not available.");
      return;
    }
    alert('Notification will be generated after a delay.');
    axios.post('http://localhost:8000/api7/create-account-activity/', {
      email_id: 'user@example.com',
      message: 'This is an account activity just for you!',
      delay: '10',  // Delay notification by 10 seconds
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(response => {
        const message = response.data.message || 'This is an account activity just for you!';
        sendNotification('Account Activity', message, './images/logo.png', 'https://www.google.com/');
        // alert('Notification will be generated after a delay.');
        // Note: The actual notification display will be delayed
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Failed to create account activity notification.');
      });
  };

  // Fetch user IDs who have account activity enabled
  useEffect(() => {
    requestNotificationPermission();

    axios.get('http://localhost:8000/api7/get-account-activity-user-ids/')
      .then(response => {
        if (response.data.user_ids && response.data.user_ids.length > 0) {
          setUserId(response.data.user_ids[0]);  // Set the first user ID
        } else {
          alert('No users with account activity enabled.');
        }
      })
      .catch(error => {
        console.error('Error fetching user IDs:', error);
      });
  }, []);

  return (
    <div>
      <main className="flex min-h-screen flex-col items-center justify-between p-24">
        <h1 className='text-4xl font-bold'>Account Activity Notification</h1>

        <button
          onClick={createImmediateNotification}
          className='bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 m-2'
        >
          Trigger Immediate Notification
        </button>

        <button
          onClick={createDelayedNotification}
          className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 m-2'
        >
          Trigger Delayed Notification
        </button>
      </main>
    </div>
  );
};

export default AccountActivity;







// 'use client';
// import React, { useEffect, useState } from 'react';
// import axios from 'axios';

// const AccountActivity = () => {
//   const [userId, setUserId] = useState('');

//   // Function to send a browser notification
//   const sendNotification = (title, message, icon, link) => {
//     if ('Notification' in window && Notification.permission === 'granted') {
//       const notification = new Notification(title, {
//         body: message, // Ensure the message is set correctly
//         icon: icon,    // Ensure the icon is set correctly
//       });

//       // Handle notification click event
//       notification.onclick = () => {
//         window.open(link, '_blank');
//       };
//     }
//   };

//   // Function to request notification permission from the user
//   const requestNotificationPermission = () => {
//     if ('Notification' in window && Notification.permission !== 'granted') {
//       Notification.requestPermission().then(permission => {
//         if (permission !== 'granted') {
//           alert('Notification permissions are not granted. Please enable them in your browser settings.');
//         }
//       });
//     }
//   };

//   // Function to create and trigger the AccountActivity notification
//   const createAccountActivityNotification = () => {
//     if (!userId) {
//       alert("User ID is not available.");
//       return;
//     }

//     axios.post('http://localhost:8000/api7/create-account-activity/', {
//       email_id: 'user@example.com',  // Adjust this to dynamically fetch user email if needed
//       message: 'This is a account activity just for you!',
//     }, {
//       headers: {
//         'Content-Type': 'application/json',
//       },
//     })
//       .then(response => {
//         // Extract message from the response or use default message
//         const message = response.data.message || 'This is a account activity just for you!';
//         // Send notification
//         sendNotification('Account Activity', message, './images/logo.png', 'https://www.accountactivity.inc/');
//       })
//       .catch(error => {
//         console.error('Error:', error);
//         alert('Failed to create account activity notification.');
//       });
//   };

//   // Fetch user IDs who have account activity enabled
//   useEffect(() => {
//     requestNotificationPermission();  // Request notification permission when component mounts

//     axios.get('http://localhost:8000/api7/get-account-activity-user-ids/')
//       .then(response => {
//         if (response.data.user_ids && response.data.user_ids.length > 0) {
//           setUserId(response.data.user_ids[0]);  // Set the first user ID
//         } else {
//           alert('No users with account activity enabled.');
//         }
//       })
//       .catch(error => {
//         console.error('Error fetching user IDs:', error);
//       });
//   }, []);

//   return (
//     <div>
//       <main className="flex min-h-screen flex-col items-center justify-between p-24">
//         <h1 className='text-4xl font-bold'>Account Activity Notification</h1>
//         <button
//           onClick={createAccountActivityNotification}
//           className='bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4'
//         >
//           Trigger Account Activity Notification
//         </button>
//       </main>
//     </div>
//   );
// };

// export default AccountActivity;
