import { useState } from 'react';
import { OnboardingForm } from './components/onboarding/OnboardingForm';
import { ChatInterface } from './components/chat/ChatInterface';

function App() {
  const [isOnboarded, setIsOnboarded] = useState(false);

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