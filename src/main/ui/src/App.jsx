import { useState } from 'react';
import { OnboardingForm } from './components/onboarding/OnboardingForm';
import { ChatInterface } from './components/chat/ChatInterface';
import LandingPage from './components/landing/LandingPage';

function App() {
  const [isLanded, setIsLanded] = useState(false);
  const [isOnboarded, setIsOnboarded] = useState(false);

  if (!isLanded) {
    return <LandingPage onComplete={() => setIsLanded(true)} />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {!isOnboarded ? (
        <OnboardingForm onComplete={() => setIsOnboarded(true)} />
      ) : (
        <ChatInterface />
      )}
    </div>
  );
}

export default App;