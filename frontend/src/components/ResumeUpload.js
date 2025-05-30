import React, { useState } from 'react';
import axios from 'axios';

function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [parsed, setParsed] = useState(null);

  const uploadResume = async () => {
    const formData = new FormData();
    formData.append("file", file);
    const res = await axios.post("http://localhost:8000/upload_resume", formData);
    setParsed(res.data.parsed_resume);
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <input type="file" onChange={(e) => setFile(e.target.files[0])} className="mb-4" />
      <button onClick={uploadResume} className="bg-blue-500 text-white px-4 py-2">Upload Resume</button>
      {parsed && (
        <pre className="mt-4 bg-gray-100 p-4 rounded text-sm">
          {JSON.stringify(parsed, null, 2)}
        </pre>
      )}
    </div>
  );
}

export default ResumeUpload;