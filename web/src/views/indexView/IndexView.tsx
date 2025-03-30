import { Link } from "react-router-dom";
import ApiClient from "../../lib/services/apiClient.ts";
import ServiceManager from "../../lib/serviceManager.ts";
import { useEffect, useState } from "react";
import {CustomTrack} from "../../lib/api/dtos.ts";
import CustomTrackListGrid from "../../components/CustomTrackListGrid.tsx";
import Typography from "@mui/material/Typography/Typography";
import Stack from "@mui/material/Stack/Stack";
import randomSlice from "../../utils/randomSlice.ts";
import Grid from "@mui/material/Grid/Grid";
import DiscordWidget from "../../components/DiscordWidget.tsx";

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
        <Grid container spacing={2}>
            <Grid item xs={12} md={9}>
                <Stack spacing={2}>
                    <Typography variant="h4">
                        Welcome!
                    </Typography>

                    <Typography variant="body1">
                        On this website you can browse and share custom tracks for CTR. Please keep in mind that
                        registration is only possible on <Link
                        to="https://records.project-saphi.com">records.project-saphi.com</Link>.
                    </Typography>

                    <Typography variant="body1">
                        The current version of the website is kind of a work in progress and will be improved as time goes on and
                        player needs change. For now, there are a few things I have planned to add in the near future:
                    </Typography>

                    <ul>
                        <li>Settings Editor (for Administrators)</li>
                        <li>Extended User Permissions (so that trusted users can upload tracks which are immediately verified)</li>
                        <li>Beta Versions (tracks that can still be updated after upload until they are final)</li>
                        <li>Language Switch (especially support for German and Spanish)</li>
                        <li>... and some other things</li>
                    </ul>

                    <Typography variant="body1">
                        I hope you enjoy using the website and, by extension, playing the Saphi mod of CTR.
                    </Typography>

                    <Typography variant="body1">
                        - Garma
                    </Typography>

                    {highlightedTracks.length > 0 && (
                        <>
                            <Stack spacing={2}>
                                <Typography>
                                    And now, enjoy some of the highest quality tracks that the community has to offer ...
                                </Typography>
                                <CustomTrackListGrid customTracks={highlightedTracks}/>
                            </Stack>
                        </>
                    )}
                </Stack>
            </Grid>

            <Grid item xs={12} md={3}>
                <DiscordWidget />
            </Grid>
        </Grid>
    );
}

export default IndexView;