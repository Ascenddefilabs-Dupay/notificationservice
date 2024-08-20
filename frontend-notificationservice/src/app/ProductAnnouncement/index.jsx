'use client';
import React, { useEffect, useCallback, useState } from 'react';
import axios from 'axios';

const Index = () => {
  const [userId, setUserId] = useState('');

  const sendNotification = (title, message, icon, link) => {
    if ('Notification' in window && Notification.permission === 'granted') {
      const notification = new Notification(title, {
        body: message,
        icon: icon,
      });

      notification.addEventListener('click', () => {
        window.open(link, '_blank');
      });
    }
  };

  const createMessageNotification = () => {
    axios.post('http://localhost:8000/api2/api2/create-message-notification/', {
      email_id: 'user@example.com',
      message: 'This is your message notification!!',
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(response => {
        sendNotification('Message Notification', response.data[0].message, './images/logo.png', 'https://console.firebase.google.com/u/0/project/registration-database-c2085/notification/compose?campaignId=2649036884902436607');
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Failed to create message notification');
      });
  };

  const createProductAnnouncementNotification = () => {
    axios.post('http://localhost:8000/api3/api3/create-product-announcement-notification/', {
      email_id: 'user@example.com',
      message: 'This is your product announcement!!',
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(response => {
        sendNotification('Product Announcement', response.data[0].message, './images/logo.png', 'https://console.firebase.google.com/u/0/project/registration-database-c2085/notification/compose?campaignId=2649036884902436607');
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Failed to create product announcement notification');
      });
  };

  const requestNotificationPermission = useCallback(() => {
    if ('Notification' in window) {
      if (Notification.permission === 'default') {
        Notification.requestPermission().then(permission => {
          if (permission === 'granted') {
            console.log('Notification permission granted.');
          } else {
            alert('Notification permission is denied or ignored. Please enable notifications in your browser settings.');
          }
        });
      }
    }
  }, []);

  useEffect(() => {
    requestNotificationPermission();
  }, [requestNotificationPermission]);

  return (
    <div>
      <main className="flex min-h-screen flex-col items-center justify-between p-24">
        <h1 className='text-4xl font-bold'>Notifications</h1>
        {/* <button
          onClick={createMessageNotification}
          className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 m-2'
        >
          Trigger Message Notification
        </button> */}
        <button
          onClick={createProductAnnouncementNotification}
          className='bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 m-2'
        >
          Trigger Product Announcement Notification
        </button>
      </main>
    </div>
  );
};

export default Index;
