import styled from "@emotion/styled";
import {Box} from "@mui/material";

export const YoutubeVideoContainer = styled(Box)`
    position: relative;
    overflow: hidden;
    max-width: 640px;

    &::after {
        display: block;
        content: "";
        padding-top: 56.25%;
    }

    iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }
`;
