// src/app/EmailVerification/index.jsx
import { useState } from 'react';
import EmailForm from './EmailForm';
import OtpForm from './OtpForm';

const EmailVerification = () => {
  const [email, setEmail] = useState('');
  const [step, setStep] = useState(1);

  const handleEmailSent = (email) => {
    setEmail(email);
    setStep(2);
  };

  return (
    <div>
      {step === 1 && <EmailForm onEmailSent={handleEmailSent} />}
      {step === 2 && <OtpForm email={email} />}
    </div>
  );
};

export default EmailVerification;
