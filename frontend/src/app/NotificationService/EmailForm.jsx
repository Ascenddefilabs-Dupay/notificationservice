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
      <h2>Let's Verify Your Details</h2>
      <div className="form-group">
        <label>Email Address*</label>
        <div className="email-input-container">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
          />
          <button onClick={handleEmailSubmit}>Send OTP</button>
        </div>
      </div>
      {/* <div className="form-group">
        <input type="checkbox" />
        <label>
          Yes, I would like to be kept up to date with promotions and marketing. (You can opt out at any time.)
        </label>
      </div>
      <div className="form-group">
        <input type="checkbox" />
        <label>
          I have read and agree to the <a href="#">Terms and Conditions</a> and <a href="#">Privacy Policy</a>.
        </label>
      </div> */}
      {/* <button className="continue-button">Continue</button> */}
      <p>{message}</p>
    </div>
  );
};

export default EmailForm;


// import React, { useState } from 'react';
// import axios from 'axios';
// import './EmailForm.css';

// const EmailForm = ({ onEmailSent }) => {
//   const [email, setEmail] = useState('');
//   const [message, setMessage] = useState('');

//   const handleEmailSubmit = async () => {
//     try {
//       const response = await axios.post('http://localhost:8000/api/verify-email/', { email_id: email });
//       setMessage(response.data.message);
//       onEmailSent(email);
//     } catch (error) {
//       setMessage(error.response?.data?.error || 'An error occurred');
//     }
//   };

//   return (
//     <div className="email-form-container">
//       <input
//         type="email"
//         value={email}
//         onChange={(e) => setEmail(e.target.value)}
//         placeholder="Enter your email"
//       />
//       <button onClick={handleEmailSubmit}>Verify Email</button>
//       <p>{message}</p>
//     </div>
//   );
// };

// export default EmailForm;
