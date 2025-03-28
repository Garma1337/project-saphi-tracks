import { Link } from "react-router-dom";
import ApiClient from "../../lib/services/apiClient.ts";
import ServiceManager from "../../lib/serviceManager.ts";
import { useEffect, useState } from "react";
import {CustomTrack} from "../../lib/api/dtos.ts";
import CustomTrackListGrid from "../../components/CustomTrackListGrid.tsx";
import Typography from "@mui/material/Typography/Typography";
import Stack from "@mui/material/Stack/Stack";
import randomSlice from "../../utils/randomSlice.ts";

const IndexView = () => {
    const apiClient: ApiClient = ServiceManager.createApiClient();

    const [highlightedTracks, setHighlightedTracks] = useState<CustomTrack[]>([]);

    useEffect(() => {
        apiClient.findCustomTracks(null, null, null, true, null, 1, 10).then((query) => {
            const items = query.items || [];
            const randomTracks: CustomTrack[] = randomSlice(items, 3);

            setHighlightedTracks(randomTracks);
        });
    }, [setHighlightedTracks]);

    return (
        <>
            Welcome to the track repository for Project Saphi!
            <br/><br/>
            On this website you can browse and share custom tracks for the game. However, please keep in mind that
            registration is only possible on <Link to="https://records.project-saphi.com">records.project-saphi.com</Link>.
            <br/><br/>
            The current version of the website is kind of a work in progress and will be improved as time goes on and player
            needs change. For now, there are a few things I have planned to add in the near future:

            <ul>
                <li>Settings Editor (for Administrators)</li>
                <li>Extended User Permissions (so that trusted users can upload tracks which are immediately verified)</li>
                <li>Beta Versions (tracks that can still be updated after upload until they are final)</li>
                <li>Language Switch (especially support for German and Spanish)</li>
                <li>... and some other things</li>
            </ul>

            - Garma

            {highlightedTracks.length > 0 && (
                <>
                    <br/><br/>
                    <Stack spacing={2}>
                        <Typography>
                            And now, enjoy some of the highest quality tracks that the community has to offer ...
                        </Typography>
                        <CustomTrackListGrid customTracks={highlightedTracks}/>
                    </Stack>
                </>
            )}
        </>
    );
}

export default IndexView;