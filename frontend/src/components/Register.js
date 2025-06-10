import React, { useState } from 'react';

function Register() {
  const [form, setForm] = useState({
    name: '',
    username: '',
    password: '',
    email: '',
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    const res = await fetch("http://localhost:8000/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });

    const data = await res.json();
    if (res.ok) {
      alert("Account created!");
    } else {
      alert(data.detail || "Registration failed.");
    }
  };

  return (
    <div className="p-6 max-w-sm mx-auto">
      <h2 className="text-xl font-semibold mb-4">Register</h2>
      <input
        name="name"
        onChange={handleChange}
        placeholder="Name"
        className="block w-full p-2 mb-2 border"
      />
      <input
        name="username"
        onChange={handleChange}
        placeholder="Username"
        className="block w-full p-2 mb-2 border"
      />
      <input
        name="email"
        type="email"
        onChange={handleChange}
        placeholder="Email"
        className="block w-full p-2 mb-2 border"
      />
      <input
        name="password"
        type="password"
        onChange={handleChange}
        placeholder="Password"
        className="block w-full p-2 mb-2 border"
      />
      <button
        onClick={handleSubmit}
        className="bg-green-600 text-white px-4 py-2"
      >
        Register
      </button>
    </div>
  );
}

export default Register;
