export const Message = ({ content, isUser }) => (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`max-w-[80%] rounded-lg p-4 ${
        isUser ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-800'
      }`}>
        {content}
      </div>
    </div>
  );