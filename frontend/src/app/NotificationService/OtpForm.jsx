import React, { useState, useEffect } from 'react';
import axiosInstance from '../../utils/axiosInstance';
import './OtpForm.css';

const OtpForm = ({ email }) => {
  const [otp, setOtp] = useState('');
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');
  const [timer, setTimer] = useState(30);
  const [isResendDisabled, setIsResendDisabled] = useState(true);

  const handleOtpSubmit = async () => {
    try {
      const response = await axiosInstance.put('/api/verify-email/', { email_id: email, otp });
      setMessage(response.data.message);
      setMessageType('success');
    } catch (error) {
      setMessage(error.response?.data?.error || 'An error occurred');
      setMessageType('error');
    }
  };

  const handleResendOtp = async () => {
    try {
      await axiosInstance.post('/api/verify-email/', { email_id: email });
      setMessage('OTP has been resent.');
      setMessageType('info');
      setIsResendDisabled(true);
      setTimer(30);
    } catch (error) {
      setMessage('Failed to resend OTP.');
      setMessageType('error');
    }
  };

  useEffect(() => {
    if (isResendDisabled) {
      const interval = setInterval(() => {
        setTimer((prev) => {
          if (prev === 1) {
            setIsResendDisabled(false);
            clearInterval(interval);
            return 30;
          }
          return prev - 1;
        });
      }, 1000);
    }
  }, [isResendDisabled]);

  return (
    <div className="otp-form-container">
      <h2>Verify OTP</h2>
      <input
        type="text"
        style={{ color: 'black' }}
        value={otp}
        onChange={(e) => setOtp(e.target.value)}
        placeholder="Enter OTP"
      />
      <div className="button-container">
        <button onClick={handleResendOtp} disabled={isResendDisabled}>
          Resend OTP{isResendDisabled && `(${timer}s)`}
        </button>
        <button onClick={handleOtpSubmit}>Verify OTP</button>
      </div>
      <button className="continue-button1">Continue</button>
      <p className={`message ${messageType}`}>{message}</p>
    </div>
  );
};

export default OtpForm;


// import React, { useState } from 'react';
// import axiosInstance from '../../utils/axiosInstance';
// import './OtpForm.css';

// const OtpForm = ({ email }) => {
//   const [otp, setOtp] = useState('');
//   const [message, setMessage] = useState('');

//   const handleOtpSubmit = async () => {
//     try {
//       const response = await axiosInstance.put('/api/verify-email/', { email_id: email, otp });
//       setMessage(response.data.message);
//     } catch (error) {
//       setMessage(error.response?.data?.error || 'An error occurred');
//     }
//   };

//   return (
//     <div className="otp-form-container">
//       <input
//         type="text"
//         value={otp}
//         onChange={(e) => setOtp(e.target.value)}
//         placeholder="Enter OTP"
//       />
//       <button onClick={handleOtpSubmit}>Verify OTP</button>
//       <p>{message}</p>
//     </div>
//   );
// };

// export default OtpForm;
