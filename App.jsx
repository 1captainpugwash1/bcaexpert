import React, { useState } from 'react';
import WelcomeScreen from './components/WelcomeScreen';
import ChatInterface from './components/ChatInterface';
import './App.css';

function App() {
  const [showChat, setShowChat] = useState(false);
  const [initialQuery, setInitialQuery] = useState('');

  const handleStartChat = (query = '') => {
    setInitialQuery(query);
    setShowChat(true);
  };

  return (
    <div className="App">
      {!showChat ? (
        <WelcomeScreen onStartChat={handleStartChat} appName="BCA Expert App" />
      ) : (
        <ChatInterface initialQuery={initialQuery} appName="BCA Expert App" />
      )}
    </div>
  );
}

export default App;

