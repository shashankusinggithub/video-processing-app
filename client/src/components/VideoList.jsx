import React, { useState, useEffect } from "react";
import axios from "axios";
import VideoPlayer from "./VideoPlayer";
function VideoList() {
  const [videos, setVideos] = useState([]);
  const [videoObj, setVideoObj] = useState({});
  const [key, setKey] = useState(0);

  useEffect(() => {
    const fetchVideos = async () => {
      const response = await axios.get("/api/videos/");
      setVideos(response.data.videos || []);
    };

    fetchVideos();
  }, []);

  const handleClick = (video, ind) => {
    setVideoObj(video);
    setKey(ind);
  };

  return (
    <>
      <div className="w-full">
        {videoObj.title && (
          <VideoPlayer videoObj={videoObj} key={key} className="w-full" />
        )}
      </div>

      <div className="relative overflow-x-auto shadow-md sm:rounded-lg m-10">
        <h3>Uploaded Videos</h3>
        <table class="w-full text-sm text-left rtl:text-right text-gray-500">
          <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-300 dark:text-gray-900">
            <tr>
              <th scope="col" className="px-6 py-3">
                Title
              </th>
              <th scope="col" className="px-6 py-3">
                Uploaded At
              </th>
              <th scope="col" className="px-6 py-3"></th>
            </tr>
          </thead>
          <tbody>
            {videos.map((video, ind) => {
              return (
                <tr className="bg-white  dark:bg-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-00">
                  <td className="px-6 py-3">{video.title}</td>
                  <td className="px-6 py-3">
                    {new Date(video.uploaded_at).toLocaleString()}
                  </td>
                  <button
                    className="px-6 py-3"
                    onClick={() => {
                      handleClick(video, ind);
                    }}
                  >
                    Play
                  </button>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </>
  );
}

export default VideoList;
