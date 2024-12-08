const API_URL = import.meta.env.VITE_API_URL;

export const api = {
  async sendMessage(message, mood) {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, mood })
    });
    
    if (!response.ok) {
      throw new Error('API request failed');
    }
    
    return response.json();
  },

  async saveProfile(profile) {
    const response = await fetch(`${API_URL}/profile`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(profile)
    });
    
    if (!response.ok) {
      throw new Error('Failed to save profile');
    }
    
    return response.json();
  }
}; 