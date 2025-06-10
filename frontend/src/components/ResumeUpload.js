import React, { useState, useEffect } from 'react';

function ResumeUpload({ userId }) {
  const [file, setFile] = useState(null);
  const [resumeData, setResumeData] = useState(null);

  const fetchResumeData = async () => {
    if (!userId) return;
    const res = await fetch(`http://localhost:8000/resume_data/${userId}`);
    const data = await res.json();
    if (res.ok) {
      try {
        if (typeof data.skills === "string") {
          data.skills = JSON.parse(data.skills);
        }
      } catch {
        data.skills = [];
      }
      setResumeData(data);
    }
  };

  useEffect(() => {
    fetchResumeData();
  }, [userId]);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', userId);

    const res = await fetch('http://localhost:8000/upload_resume', {
      method: 'POST',
      body: formData,
    });

    if (res.ok) {
      alert("Resume uploaded and parsed.");
      await new Promise((resolve) => setTimeout(resolve, 500));
      fetchResumeData(); // re-fetch after DB is updated
    } else {
      const data = await res.json();
      alert(data.detail || 'Upload failed');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-10 px-4 flex justify-center">
      <div className="w-full max-w-5xl bg-white rounded-xl shadow-lg p-8 border border-gray-200">
        <h1 className="text-4xl font-bold mb-10 text-center text-gray-900">📄 Resume Analyzer</h1>

        {/* Upload section */}
        <div className="flex flex-col md:flex-row items-center gap-4 mb-10">
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            className="block w-full md:w-auto text-sm text-gray-700 border border-gray-300 rounded-md cursor-pointer bg-white px-4 py-2 shadow-sm hover:border-blue-400 transition"
          />
          <button
            onClick={handleUpload}
            disabled={!file}
            className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-semibold px-6 py-2 rounded shadow transition"
          >
            Upload Resume
          </button>
        </div>

        {/* File name preview */}
        {file && (
          <div className="mb-6 text-sm text-gray-600">
            <strong>Selected File:</strong> {file.name}
          </div>
        )}

        {/* Resume data */}
        <h2 className="text-2xl font-semibold mb-6 text-gray-800 border-b pb-2">📋 Parsed Resume Data</h2>

        {resumeData ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-gray-700 text-base">
            <p><strong>Name:</strong> {resumeData.name || "N/A"}</p>
            <p><strong>Email:</strong> {resumeData.email || "N/A"}</p>
            <p><strong>Phone:</strong> {resumeData.mobile_number || "N/A"}</p>
            <p><strong>College:</strong> {resumeData.college_name || "N/A"}</p>
            <p><strong>Degree:</strong> {resumeData.degree || "N/A"}</p>
            <p><strong>Designation:</strong> {resumeData.designation || "N/A"}</p>
            <p className="md:col-span-2"><strong>Company Names:</strong> {resumeData.company_names || "N/A"}</p>

            <div className="md:col-span-2 mt-2">
              <h3 className="font-semibold text-lg mb-2 flex items-center gap-1">🛠 Skills</h3>
              {Array.isArray(resumeData.skills) && resumeData.skills.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                  {resumeData.skills.map((skill, i) => (
                    <span
                      key={i}
                      className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm shadow-sm"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-sm">No skills found.</p>
              )}
            </div>

            <div className="md:col-span-2 mt-6">
              <h3 className="font-semibold text-lg mb-2 flex items-center gap-1">💼 Experience</h3>
              <div className="bg-gray-50 border rounded-lg p-4 text-sm whitespace-pre-wrap font-mono text-gray-800">
                {resumeData.experience || "No experience data found."}
              </div>
            </div>
          </div>
        ) : (
          <p className="text-gray-500 text-center">No resume data available yet. Please upload a file.</p>
        )}
      </div>
    </div>
  );
}

export default ResumeUpload;
