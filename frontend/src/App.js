import React, { useState } from 'react';
import ResumeUpload from './components/ResumeUpload';
import Login from './components/Login';
import Register from './components/Register';

function App() {
  const [userId, setUserId] = useState(null);
  const [view, setView] = useState("login"); // or "register" or "upload"

  const renderView = () => {
    if (!userId) {
      if (view === "login") return <Login setUserId={setUserId} />;
      if (view === "register") return <Register />;
    }
    return <ResumeUpload userId={userId} />;
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="mb-4 space-x-4">
        {!userId && (
          <>
            <button onClick={() => setView("login")} className="underline text-blue-600">Login</button>
            <button onClick={() => setView("register")} className="underline text-green-600">Register</button>
          </>
        )}
      </div>
      {renderView()}
    </div>
  );
}

export default App;
