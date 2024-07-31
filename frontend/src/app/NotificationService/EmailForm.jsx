import React, { useState } from 'react';
import axios from 'axios';
import './EmailForm.css';

const EmailForm = ({ onEmailSent }) => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');

  const handleEmailSubmit = async () => {
    try {
      const response = await axios.post('http://localhost:8000/api/verify-email/', { email_id: email });
      setMessage(response.data.message);
      onEmailSent(email);
    } catch (error) {
      setMessage(error.response?.data?.error || 'An error occurred');
    }
  };

  return (
    <div className="email-form-container">
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Enter your email"
      />
      <button onClick={handleEmailSubmit}>Verify Email</button>
      <p>{message}</p>
    </div>
  );
};

export default EmailForm;
