import React from 'react';
import ResumeUpload from './components/ResumeUpload';

function App() {
  return (
    <div className="min-h-screen bg-white p-8">
      <h1 className="text-2xl font-bold mb-4">CareerMapAI Resume Parser</h1>
      <ResumeUpload />
    </div>
  );
}

export default App;