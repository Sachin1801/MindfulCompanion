export const Message = ({ content, isUser, crisisResources }) => (
  <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
    <div className={`max-w-[80%] rounded-lg p-4 ${
      isUser ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-800'
    }`}>
      <div>{content}</div>
      
      {crisisResources && (
        <div className="mt-4 p-4 bg-red-50 rounded-lg border border-red-200">
          <h4 className="font-semibold text-red-700 mb-2">Available Resources:</h4>
          <ul className="list-disc pl-4 space-y-1">
            {crisisResources.map((resource, idx) => (
              <li key={idx} className="text-red-600">{resource}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  </div>
);