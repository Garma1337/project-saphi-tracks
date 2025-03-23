import {useEffect, useState} from "react";
import getYoutubeVideoCode from "../utils/getYouTubeVideoCode.ts";
import {YoutubeVideoContainer} from "../views/layout/Layout.styles.ts";

interface YoutubeVideoProperties {
    src: string;
    width?: number;
    height?: number;
}

const YouTubeVideo = (properties: YoutubeVideoProperties) => {
    const [videoCode, setVideoCode] = useState<string | null>(null);

    useEffect(() => {
        const videoCode = getYoutubeVideoCode(properties.src);
        setVideoCode(videoCode);
    }, [properties, setVideoCode]);

    return (
        <YoutubeVideoContainer>
            <iframe
                width={properties.width || 640}
                height={properties.height || 480}
                src={`https://www.youtube.com/embed/${videoCode}`}
                title="YouTube Video Player"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
            ></iframe>
        </YoutubeVideoContainer>
    );
}

export default YouTubeVideo;
