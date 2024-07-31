import React, { useState } from 'react';
import axiosInstance from '../../utils/axiosInstance';
import './OtpForm.css';

const OtpForm = ({ email }) => {
  const [otp, setOtp] = useState('');
  const [message, setMessage] = useState('');

  const handleOtpSubmit = async () => {
    try {
      const response = await axiosInstance.put('/api/verify-email/', { email_id: email, otp });
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data?.error || 'An error occurred');
    }
  };

  return (
    <div className="otp-form-container">
      <input
        type="text"
        value={otp}
        onChange={(e) => setOtp(e.target.value)}
        placeholder="Enter OTP"
      />
      <button onClick={handleOtpSubmit}>Verify OTP</button>
      <p>{message}</p>
    </div>
  );
};

export default OtpForm;
