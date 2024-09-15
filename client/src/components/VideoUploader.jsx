import React, { useState } from "react";
import axios from "axios";
// axios.defaults.baseURL = "http://localhost:8000";

const VideoUploader = () => {
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState("");
  const [dragging, setDragging] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    setFile(e.dataTransfer.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("video_file", file);
    formData.append("title", title);
    try {
      await axios.post("/api/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      window.location.reload();
    } catch (error) {
      alert("Unable to extract video");
    }
  };

  return (
    <>
      <div className="flex flex-col items-center p-6 bg-gray-100 rounded-lg shadow-lg w-full max-w-md mx-auto">
        <h2 className="text-xl font-semibold mb-4">Upload a File</h2>

        <input
          type="text"
          placeholder="Enter title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="border rounded p-2 w-full mb-4"
        />

        <div
          className={`border-2 py-16 w-full rounded mb-4 ${
            dragging ? "border-blue-500 bg-blue-100" : "border-gray-300"
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <input
            type="file"
            onChange={handleFileChange}
            className="hidden"
            id="file-input"
          />
          <label
            htmlFor="file-input"
            className="cursor-pointer flex justify-center items-center"
          >
            {file ? (
              <p>{file.name}</p>
            ) : (
              <p className="text-gray-500">
                Drag & drop a file here or click to upload
              </p>
            )}
          </label>
        </div>

        <button
          onClick={handleSubmit}
          className="bg-blue-500 text-white px-4 py-2 rounded w-full hover:bg-blue-600"
        >
          Upload
        </button>
      </div>
    </>
  );
};

export default VideoUploader;
