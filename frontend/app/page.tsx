// pages/index.tsx or pages/page.tsx
import { GoogleOAuthProvider } from '@react-oauth/google';
import GoogleLoginButton from '../components/GoogleLoginButton';

const Page = () => {
  return (
    <GoogleOAuthProvider clientId="991081744124-t2t98f0hfeqkccejmrp560lkiq7ftukp.apps.googleusercontent.com">
      <div>
        <h1>Login with Google</h1>
        <GoogleLoginButton />
      </div>
    </GoogleOAuthProvider>
  );
};

export default Page;