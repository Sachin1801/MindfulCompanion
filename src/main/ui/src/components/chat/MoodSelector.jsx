
export const MoodSelector = ({ value, onChange }) => (
    <select 
      value={value} 
      onChange={(e) => onChange(e.target.value)}
      className="p-2 rounded-lg bg-white border border-gray-300 text-gray-700 w-32"
    >
      <option value="">Current Mood</option>
      <option value="happy">Happy</option>
      <option value="motivated">Motivated</option>
      <option value="neutral">Neutral</option>
      <option value="stressed">Stressed</option>
      <option value="sad">Sad</option>
      <option value="depressed">Depressed</option>
    </select>
  );