import React, { useState, useEffect } from 'react';

function ResumeUpload({ userId }) {
  const [file, setFile] = useState(null);
  const [parsedSkills, setParsedSkills] = useState([]);

  // Fetch existing skills from DB on component mount
  useEffect(() => {
    const fetchSkills = async () => {
      if (!userId) return;
      const res = await fetch(`http://localhost:8000/resume_data/${userId}`);
      const data = await res.json();
      if (res.ok) {
        setParsedSkills(data.skills);
      }
    };
    fetchSkills();
  }, [userId]);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', userId);

    const res = await fetch('http://localhost:8000/upload_resume', {
      method: 'POST',
      body: formData,
    });

    const data = await res.json();
    if (res.ok) {
      alert("Resume uploaded and parsed.");
      setParsedSkills(data.parsed_resume || []); // fallback if backend returns parsed data
    } else {
      alert(data.detail || 'Upload failed');
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Upload Your Resume</h1>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} className="mb-4" />
      <button onClick={handleUpload} className="bg-blue-600 text-white px-4 py-2 rounded">
        Upload Resume
      </button>

      <div className="mt-6">
        <h2 className="text-lg font-semibold mb-2">Previously Parsed Skills:</h2>
        {parsedSkills.length > 0 ? (
          <ul className="list-disc ml-6">
            {parsedSkills.map((skill, i) => (
              <li key={i}>{skill}</li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-500">No resume data available yet.</p>
        )}
      </div>
    </div>
  );
}

export default ResumeUpload;
