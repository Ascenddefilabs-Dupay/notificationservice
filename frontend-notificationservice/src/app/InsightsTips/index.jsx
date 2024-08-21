'use client';
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const index = () => {
  const [userId, setUserId] = useState('');

  // Function to send a browser notification
  const sendNotification = (title, message, icon, link) => {
    if ('Notification' in window && Notification.permission === 'granted') {
      const notification = new Notification(title, {
        body: message,  // Make sure the message is set in the notification body
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

  // Function to create and trigger the Insights Tips notification
  const createInsightsTipsNotification = () => {
    if (!userId) {
      alert("User ID is not available.");
      return;
    }

    axios.post('http://localhost:8000/api5/create-insights-tips-notification/', {
      email_id: 'user@example.com',  // Adjust this to dynamically fetch user email if needed
      message: 'This is your insights tips notification!',
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(response => {
        const message = response.data.message || 'This is your insights tips notification!';
        sendNotification('Insights Tips', message, './images/logo.png', 'https://www.specialoffer.inc/');
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Failed to create Insights Tips notification.');
      });
  };

  // Fetch user IDs who have Insights Tips enabled
  useEffect(() => {
    requestNotificationPermission();  // Request notification permission when component mounts

    axios.get('http://localhost:8000/api5/get_insights_tips_user_ids/')
      .then(response => {
        if (response.data.user_ids && response.data.user_ids.length > 0) {
          setUserId(response.data.user_ids[0]);  // Set the first user ID
        } else {
          alert('No users with Insights Tips enabled.');
        }
      })
      .catch(error => {
        console.error('Error fetching user IDs:', error);
      });
  }, []);

  return (
    <div>
      <main className="flex min-h-screen flex-col items-center justify-between p-24">
        <h1 className='text-4xl font-bold'>Insights Tips Notification</h1>
        <button
          onClick={createInsightsTipsNotification}
          className='bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4'
        >
          Trigger Insights Tips Notification
        </button>
      </main>
    </div>
  );
};

export default index;