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

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    try {
      setLoading(true);
      const newMessage = { message: inputMessage, mood: currentMood };
      setMessages([...messages, { content: inputMessage, isUser: true }]);
      setInputMessage('');

      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newMessage)
      });

      const data = await response.json();
      setMessages(msgs => [...msgs, { content: data.message, isUser: false }]);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((msg, idx) => (
          <Message key={idx} content={msg.content} isUser={msg.isUser} />
        ))}
      </div>
      
      <div className="p-4 bg-white border-t">
        <div className="flex gap-2">
          <MoodSelector value={currentMood} onChange={setCurrentMood} />
          <div className="flex-1 flex gap-2">
            <Input
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Type your message..."
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            />
            <Button onClick={sendMessage} disabled={loading}>
              <Send className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};