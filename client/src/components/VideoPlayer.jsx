import axios from "axios";
import React, { useEffect, useState, useRef } from "react";
import SearchTool from "./SearchCaptions";
import Options from "./Options";

function VideoPlayer({ videoObj }) {
  const [subtitles, setSubtitles] = useState([]);
  const [activeSubtitleId, setActiveSubtitleId] = useState();

  const videoRef = useRef(null);

  useEffect(() => {
    return async () => {
      const subtitlePromises = videoObj.subtitle_ids.map((item) =>
        getSubtitleLink(item)
      );
      const subtitles_resolved = await Promise.all(subtitlePromises);

      setSubtitles(subtitles_resolved);
      setActiveSubtitleId(subtitles_resolved[0].subtitles_id);
    };
  }, [videoObj]);

  async function getSubtitleLink(item) {
    const response = await axios.get(`/api/subtitles/${item.id}/`, {
      responseType: "blob",
    });
    const subtitleUrl = URL.createObjectURL(response.data);
    return {
      subtitleUrl,
      language: item.language,
      subtitles_id: item.id,
    };
  }
  return (
    <div>
      <div className="flex flex-col items-center my-5">
        <video controls id="video_player" ref={videoRef} key={videoObj.id}>
          <source src={`/api/videos/${videoObj.id}/`} type="video/mp4" />
          {subtitles.map((item, index) => (
            <track
              key={index.subtitlesId}
              src={item.subtitleUrl}
              kind="subtitles"
              srcLang={item.language}
              label={item.language}
              default={index === 0 ? true : false}
            />
          ))}
        </video>
      </div>
      <Options
        subtitles={subtitles}
        videoRef={videoRef}
        setActiveSubtitleId={setActiveSubtitleId}
      />
      <SearchTool videoRef={videoRef} subtitleId={activeSubtitleId} />
    </div>
  );
}

export default VideoPlayer;
