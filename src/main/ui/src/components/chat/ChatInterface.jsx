import { useState } from 'react';
import { Send } from 'lucide-react';
import { Message } from './Message';
import { MoodSelector } from './MoodSelector';
import { Input } from '../common/Input';
import { Button } from '../common/Button';

export const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [currentMood, setCurrentMood] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    try {
      setLoading(true);
      setError(null);
      const newMessage = { message: inputMessage, mood: currentMood };
      
      // Optimistically add user message
      const userMessage = { content: inputMessage, isUser: true };
      setMessages(prev => [...prev, userMessage]);
      setInputMessage('');

      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newMessage)
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const data = await response.json();
      
      // Add AI response
      setMessages(prev => [...prev, { 
        content: data.message, 
        isUser: false,
        hasCrisisResources: data.crisis_resources?.length > 0,
        crisisResources: data.crisis_resources
      }]);
    } catch (error) {
      setError('Failed to send message. Please try again.');
      // Remove optimistically added message
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((msg, idx) => (
          <Message 
            key={idx} 
            content={msg.content} 
            isUser={msg.isUser}
            crisisResources={msg.crisisResources}
          />
        ))}
        {error && (
          <div className="text-red-500 text-center p-2">{error}</div>
        )}
      </div>
      
      <div className="p-4 bg-white border-t">
        <div className="flex gap-2">
          <MoodSelector value={currentMood} onChange={setCurrentMood} />
          <div className="flex-1 flex gap-2">
            <Input
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Type your message..."
              onKeyPress={(e) => e.key === 'Enter' && !loading && sendMessage()}
              disabled={loading}
            />
            <Button onClick={sendMessage} disabled={loading}>
              {loading ? (
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};