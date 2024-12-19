// components/GoogleLoginButton.tsx
'use client';

import { GoogleLogin } from '@react-oauth/google';

const GoogleLoginButton = () => {
  const handleLogin = (response) => {
    console.log(response);
    // Send the response credential to your backend for verification and user creation
    fetch(`http://localhost:8000/auth/callback?token=${response.credential}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    })
      .then((res) => res.json())
      .then((data) => console.log(data));
  };

  return (
    <GoogleLogin
      onSuccess={handleLogin}
      onError={(error) => console.log('Login Failed', error)}
    />
  );
};

export default GoogleLoginButton;
