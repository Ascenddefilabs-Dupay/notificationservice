'use client';
import React, { useEffect, useCallback } from 'react';

const Index = () => {

  const sendNotification = () => {
    if ('Notification' in window && Notification.permission === 'granted') {
      const notification = new Notification('Dupay', {
        body: 'This is your notification message!!',
        icon: './images/logo.png',
        data: {
          url: 'https://trello.com/b/gaKr5gi3/team-1' // Replace with your desired URL
        }
      });

      // Add an event listener to handle click
      notification.addEventListener('click', () => {
        window.open(notification.data.url, '_blank');
      });
    }
  };

  const requestNotificationPermission = useCallback(() => {
    if ('Notification' in window) {
      if (Notification.permission === 'default' || Notification.permission === 'denied') {
        Notification.requestPermission().then(function (permission) {
          if (permission === 'granted') {
            console.log('Notification permission granted!!');
            sendNotification();
          } else {
            console.log('Notification permission denied or ignored.');
            alert('Notification permission is denied or ignored. Please enable notifications in your browser settings.');
          }
        });
      } else if (Notification.permission === 'granted') {
        sendNotification();
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
        <h1 className='text-4xl font-bold'>hello</h1>
        <button
          onClick={sendNotification}
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

// const Index = () => {

//   const sendNotification = () => {
//     if ('Notification' in window && Notification.permission === 'granted') {
//       const notification = new Notification('Dupay', {  // Update the title here
//         body: 'This is your notification message!!',
//         icon: './images/logo.png',
//         data: {
//           url: 'https://trello.com/b/gaKr5gi3/team-1' // Replace with your desired URL
//         }
//       });

//       // Add an event listener to handle click
//       notification.addEventListener('click', () => {
//         window.open(notification.data.url, '_blank');
//       });
//     }
//   };

//   const requestNotificationPermission = useCallback(() => {
//     if ('Notification' in window) {
//       Notification.requestPermission().then(function (permission) {
//         if (permission === 'granted') {
//           console.log('Notification permission granted!!');
//           sendNotification();
//         }
//       });
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
//         <h1 className='text-4xl font-bold'>hello</h1>
//         <button
//           onClick={sendNotification}
//           className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4'
//         >
//           Trigger Notification
//         </button>
//       </main>
//     </div>
//   );
// };

// export default Index;
