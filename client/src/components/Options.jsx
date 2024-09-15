import React, { useState } from "react";

const Tabs = ({ subtitles, videoRef, setActiveSubtitleId }) => {
  const [activeTab, setActiveTab] = useState(0); // State for active tab

  const handleClick = (ind, id) => {
    // setSubtitleId(id);
    setActiveTab(ind);
    setActiveSubtitleId(id);
    const textTracks = videoRef.current.textTracks;
    if (textTracks && textTracks.length > 0) {
      for (let i = 0; i < textTracks.length; i++) {
        textTracks[i].mode = i === ind ? "showing" : "disabled";
      }
    } else {
    }
  };
  return (
    <div className="w-full max-w-md mx-auto">
      {/* Tab headers */}
      <div className="flex border-b border-gray-300">
        {subtitles.map((tab, index) => (
          <button
            key={index}
            onClick={() => handleClick(index, tab.subtitles_id)}
            className={`py-2 px-4 w-full text-center focus:outline-none ${
              activeTab === index
                ? "border-b-2 border-blue-500 text-blue-500 font-semibold"
                : "text-gray-500 hover:text-blue-500"
            }`}
          >
            {tab.language}
          </button>
        ))}
      </div>
    </div>
  );
};

export default Tabs;
