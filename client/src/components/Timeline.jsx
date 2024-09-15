import React from "react";

function Timeline({ phrases, videoRef }) {
  const changeTimeline = async (timestamp) => {
    videoRef.current.currentTime = timestamp;
  };
  return (
    <div className="m-12">
      <ol class="relative border-s border-gray-200 dark:border-gray-700">
        {phrases.map((phrase) => (
          <li
            class="mb-3 ms-4 cursor-pointer border-b border rounded p-1  hover:bg-gray-5 dark:hover:bg-gray-200"
            onClick={() => changeTimeline(phrase.timestamp)}
          >
            <div class="absolute w-3 h-3 bg-gray-200 rounded-full mt-1.5 -start-1.5 border border-white dark:border-gray-900 dark:bg-gray-700"></div>
            <time class="mb-1 text-ml font-normal leading-none text-gray-400 dark:text-gray-500">
              {phrase.timestamp}
            </time>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-black">
              {phrase.phrase}
            </h3>
          </li>
        ))}
      </ol>
    </div>
  );
}

export default Timeline;
