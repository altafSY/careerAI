import React, { useState } from 'react';
import ResumeUpload from './components/ResumeUpload';
import Login from './components/Login';
import Register from './components/Register';

function App() {
  const [userId, setUserId] = useState(null);
  const [view, setView] = useState("login");

  const handleLogout = () => {
    setUserId(null);
    setView("login");
  };

  const renderView = () => {
    if (!userId) {
      if (view === "login") return <Login setUserId={setUserId} />;
      if (view === "register") return <Register />;
    }
    return <ResumeUpload userId={userId} />;
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-start px-4 py-10">
      {/* Top bar */}
      <div className="w-full max-w-4xl flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-gray-800">CareerMapAI</h1>
        {userId ? (
          <button
            onClick={handleLogout}
            className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded shadow"
          >
            Logout
          </button>
        ) : (
          <div className="space-x-4">
            <button onClick={() => setView("login")} className="text-blue-600 underline">
              Login
            </button>
            <button onClick={() => setView("register")} className="text-green-600 underline">
              Register
            </button>
          </div>
        )}
      </div>

      {/* Main content */}
      <div className="w-full max-w-4xl">
        {renderView()}
      </div>
      <div className="bg-red-500 text-white p-4 rounded">
  If this box is red, Tailwind is working!
</div>
    </div>

  );
}

export default App;
