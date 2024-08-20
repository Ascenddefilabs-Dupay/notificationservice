
'use client';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Index = () => {
  const [userId, setUserId] = useState('');

  // Function to request notification permission
  const requestNotificationPermission = () => {
    if ('Notification' in window) {
      if (Notification.permission === 'default') {
        Notification.requestPermission().then(permission => {
          if (permission !== 'granted') {
            alert('Notification permission is denied or ignored. Please enable notifications in your browser settings.');
          }
        });
      }
    }
  };

  // Function to send the actual notification to the browser
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

  // Function to create a notification by calling the backend
  const createNotification = () => {
    if (!userId) {
      alert('User ID is not set.');
      return;
    }

    axios.post('http://localhost:8000/api2/api2/create-notification/', {
      email_id: 'user@example.com',
      message: 'This is your notification message!!',
      type: 'push notification',
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(response => {
        alert('Notification created successfully');
        sendNotification('This is your notification message!!'); // Trigger the browser notification
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Failed to create notification');
      });
  };

  // Fetch user IDs when the component mounts
  useEffect(() => {
    requestNotificationPermission(); // Ask for permission once

    axios.get('http://localhost:8000/api2/api2/get-user-ids/')
      .then(response => {
        if (response.data.user_ids && response.data.user_ids.length > 0) {
          setUserId(response.data.user_ids[0]); // Set the first user ID
        } else {
          alert('No users with messages enabled.');
        }
      })
      .catch(error => {
        console.error('Error fetching user IDs:', error);
      });
  }, []);

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
