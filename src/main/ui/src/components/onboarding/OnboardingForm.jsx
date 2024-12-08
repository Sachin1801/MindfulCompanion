import { useState } from 'react';
import { Input } from '../common/Input';
import { Button } from '../common/Button';

export const OnboardingForm = ({ onComplete }) => {
  const [formData, setFormData] = useState({
    name: '',
    age_category: '',
    emotions: [],
    therapy_status: '',
    interaction_style: '',
    stress_level: '',
    goals: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        onComplete();
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="max-w-lg mx-auto p-6 mt-8 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-center">Welcome to MindfulCompanion</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          value={formData.name}
          onChange={(e) => setFormData({...formData, name: e.target.value})}
          placeholder="Your name"
        />

        <select
          className="w-full p-2 border rounded-lg"
          value={formData.age_category}
          onChange={(e) => setFormData({...formData, age_category: e.target.value})}
        >
          <option value="">Select age range</option>
          <option value="0-12">0-12 years</option>
          <option value="12-20">12-20 years</option>
          <option value="20-40">20-40 years</option>
          <option value="40-60">40-60 years</option>
          <option value="60+">60+ years</option>
        </select>

        <select
          multiple
          className="w-full p-2 border rounded-lg"
          value={formData.emotions}
          onChange={(e) => setFormData({
            ...formData, 
            emotions: Array.from(e.target.selectedOptions, option => option.value)
          })}
        >
          <option value="worry">Worry</option>
          <option value="sadness">Sadness</option>
          <option value="loneliness">Loneliness</option>
          <option value="nervousness">Nervousness</option>
          <option value="anger">Anger</option>
          <option value="none">None of these</option>
        </select>

        <select
          className="w-full p-2 border rounded-lg"
          value={formData.therapy_status}
          onChange={(e) => setFormData({...formData, therapy_status: e.target.value})}
        >
          <option value="">Current therapy status</option>
          <option value="current">Currently in therapy</option>
          <option value="past">Previously attended therapy</option>
          <option value="never">Never attended therapy</option>
          <option value="considering">Considering therapy</option>
        </select>

        <select
          className="w-full p-2 border rounded-lg"
          value={formData.interaction_style}
          onChange={(e) => setFormData({...formData, interaction_style: e.target.value})}
        >
          <option value="">Preferred interaction style</option>
          <option value="direct">Direct and straightforward</option>
          <option value="gentle">Gentle and supportive</option>
          <option value="analytical">Analytical and logical</option>
          <option value="motivational">Motivational and encouraging</option>
        </select>

        <select
          className="w-full p-2 border rounded-lg"
          value={formData.stress_level}
          onChange={(e) => setFormData({...formData, stress_level: e.target.value})}
        >
          <option value="">Current stress level</option>
          <option value="low">Minimal stress</option>
          <option value="moderate">Moderate stress</option>
          <option value="high">High stress</option>
          <option value="severe">Severe stress</option>
        </select>

        <textarea
          className="w-full p-2 border rounded-lg"
          placeholder="What are your goals for using this companion?"
          value={formData.goals}
          onChange={(e) => setFormData({...formData, goals: e.target.value})}
        />

        <Button type="submit" className="w-full">
          Start Journey
        </Button>
      </form>
    </div>
  );
};