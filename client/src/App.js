import React from "react";
import VideoUploader from "./components/VideoUploader";
import VideoList from "./components/VideoList";

function App() {
  return (
    <>
      <div className="flex flex-col items-center mb-10">
        <h1 class="mb-2 mt-0 text-5xl font-bold leading-tight text-primary">
          Subtitle Extractor
        </h1>
      </div>
      <VideoUploader />
      <VideoList />
    </>
  );
}

export default App;
