import React, { useState, useEffect } from "react";

export default function ResumeUpload({ userId }) {
  const [file, setFile] = useState(null);
  const [resumeData, setResumeData] = useState(null);

  /* ---------------------- fetch helpers ---------------------- */
  const fetchResumeData = async () => {
    if (!userId) return;
    const res   = await fetch(`http://localhost:8000/resume_data/${userId}`);
    const data  = await res.json();
    if (!res.ok) return alert(data.detail || "Fetch failed");

    /* server now sends skills as an ARRAY → no JSON.parse needed */
    setResumeData(data);
  };

  useEffect(() => { fetchResumeData(); }, [userId]);

  /* ---------------------- upload handler --------------------- */
  const handleUpload = async () => {
    if (!file) return;
    const fd = new FormData();
    fd.append("file", file);
    fd.append("user_id", userId);

    const res  = await fetch("http://localhost:8000/upload_resume", {
      method: "POST",
      body: fd,
    });
    const body = await res.json();

    if (!res.ok) return alert(body.detail || "Upload failed");
    alert("Resume uploaded and parsed ✅");
    setTimeout(fetchResumeData, 400);              // tiny delay → DB commit
  };

  /* -------------------------- UI ----------------------------- */
  return (
    <div className="min-h-screen bg-gray-50 py-10 px-4 flex justify-center">
      <div className="w-full max-w-5xl bg-white rounded-xl shadow-lg p-8 border border-gray-200">

        <h1 className="text-4xl font-bold mb-10 text-center text-gray-900">📄 Resume Analyzer</h1>

        {/* upload */}
        <div className="flex flex-col md:flex-row items-center gap-4 mb-10">
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            className="block w-full md:w-auto text-sm text-gray-700 border border-gray-300 rounded-md
                       cursor-pointer bg-white px-4 py-2 shadow-sm hover:border-blue-400 transition"
          />
          <button
            onClick={handleUpload}
            disabled={!file}
            className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-semibold
                       px-6 py-2 rounded shadow transition"
          >
            Upload Resume
          </button>
        </div>

        {/* chosen file preview */}
        {file && (
          <p className="mb-6 text-sm text-gray-600">
            📁 <strong>{file.name}</strong>
          </p>
        )}

        {/* parsed data */}
        <h2 className="text-2xl font-semibold mb-6 text-gray-800 border-b pb-2">
          📋 Parsed Resume Data
        </h2>

        {resumeData ? (
          <div className="space-y-10 text-gray-800 text-base">

            {/* basics */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <p><strong>Name:</strong> {resumeData.name || "N/A"}</p>
              <p><strong>Email:</strong> {resumeData.email || "N/A"}</p>
              <p><strong>Phone:</strong> {resumeData.mobile_number || "N/A"}</p>
              <p><strong>College:</strong> {resumeData.college_name || "N/A"}</p>
              <p><strong>Degree:</strong> {resumeData.degree || "N/A"}</p>
              <p><strong>Designation:</strong> {resumeData.designation || "N/A"}</p>
              <p className="md:col-span-2"><strong>Company Names:</strong> {resumeData.company_names || "N/A"}</p>
            </div>

            {/* skills */}
            <section>
              <h3 className="font-semibold text-lg mb-2">🛠 Skills</h3>
              {resumeData.skills?.length ? (
                <ul className="flex flex-wrap gap-2">
                  {resumeData.skills.map((s, i) => (
                    <li key={i} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm shadow-sm">
                      {s}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500 text-sm">No skills found.</p>
              )}
            </section>

            {/* experience */}
            <section>
              <h3 className="font-semibold text-lg mb-4">💼 Experience</h3>
              {resumeData.experiences?.length ? (
                <div className="space-y-6">
                  {resumeData.experiences.map((job, idx) => (
                    <div key={idx} className="border rounded-lg p-4 bg-gray-50">
                      <p className="font-medium mb-2">{job.header}</p>
                      {job.bullets?.length ? (
                        <ul className="list-disc ml-5 space-y-1">
                          {job.bullets.map((b, i) => <li key={i}>{b}</li>)}
                        </ul>
                      ) : (
                        <p className="text-gray-500 text-sm italic">No details provided.</p>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-sm">No experience data found.</p>
              )}
            </section>
          </div>
        ) : (
          <p className="text-gray-500 text-center">No resume data yet. Upload a file to get started.</p>
        )}
      </div>
    </div>
  );
}
