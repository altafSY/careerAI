import React, { useState } from 'react';

function Login({ setUserId }) {
  const [form, setForm] = useState({ username: '', password: '' });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    const res = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });

    const data = await res.json();
    if (res.ok) {
      alert("Login successful!");
      setUserId(data.user_id);
    } else {
      alert(data.detail || "Login failed.");
    }
  };

  return (
    <div className="p-6 max-w-sm mx-auto">
      <h2 className="text-xl font-semibold mb-4">Login</h2>
      <input name="username" onChange={handleChange} placeholder="Username" className="block w-full p-2 mb-2 border" />
      <input name="password" type="password" onChange={handleChange} placeholder="Password" className="block w-full p-2 mb-2 border" />
      <button onClick={handleSubmit} className="bg-blue-500 text-white px-4 py-2">Login</button>
    </div>
  );
}

export default Login;
