import { useState } from 'react';
import './LandingPage.css';

const LandingPage = ({ onComplete }) => {
  const handleClick = () => {
    onComplete();
  };

  return (
    <div className="landing-container" onClick={handleClick}>
      <div className="content">
        <div className="hello">Mindful
          <span className="hidden">Your True Companion</span>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;