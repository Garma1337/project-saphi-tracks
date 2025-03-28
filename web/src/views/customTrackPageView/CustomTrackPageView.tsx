import Stack from "@mui/material/Stack/Stack";
import Typography from "@mui/material/Typography/Typography";
import ApiClient from "../../lib/services/apiClient.ts";
import ServiceManager from "../../lib/serviceManager.ts";
import {useEffect, useState} from "react";
import {CustomTrack} from "../../lib/api/dtos.ts";
import {useSearchParams} from "react-router-dom";
import Alert from "@mui/material/Alert/Alert";
import Box from "@mui/material/Box/Box";
import Accordion from "@mui/material/Accordion/Accordion";
import AccordionDetails from "@mui/material/AccordionDetails/AccordionDetails";
import AccordionSummary from "@mui/material/AccordionSummary/AccordionSummary";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import YouTubeVideo from "../../components/YouTubeVideo.tsx";
import DownloadResourceLink from "../../components/ResourceDownloadButton.tsx";

const CustomTrackPageView = () => {
    const apiClient: ApiClient = ServiceManager.createApiClient();

    const [searchParams] = useSearchParams();
    const [customTrack, setCustomTrack] = useState<CustomTrack | null>(null);

    useEffect(() => {
        const id = Number(searchParams.get('id'));
        apiClient.findCustomTracks(id, null, null, null, null, null, null).then((query) => {
            setCustomTrack(query.items[0]);
        });
    }, [searchParams, setCustomTrack]);

    return (
        <Stack spacing={2}>
            <Typography variant="h4">Custom Track Page</Typography>

            {customTrack && (
                <Stack spacing={2}>
                    <Typography>{customTrack.name}</Typography>

                    <YouTubeVideo src={customTrack.video}/>

                    In {customTrack.author.username}'s own words:
                    <Box sx={{ bgcolor: 'background.paper' }}>
                        <Typography>"{customTrack.description}"</Typography>
                    </Box>

                    <Accordion>
                        <AccordionSummary
                            expandIcon={<ExpandMoreIcon/>}
                            aria-controls="panel1-content"
                            id="panel1-header"
                        >
                            <Typography component="span">Downloads</Typography>
                        </AccordionSummary>
                        <AccordionDetails>
                            <ul>
                                {customTrack.resources.map((resource) => (
                                    <li>
                                        <DownloadResourceLink resourceId={resource.id} label={resource.file_name} /> (v{resource.version})
                                    </li>
                                ))}
                            </ul>
                        </AccordionDetails>
                    </Accordion>
                </Stack>
            )}
            {!customTrack && <Alert severity="warning">No custom track found.</Alert>}
        </Stack>
    );
}

export default CustomTrackPageView;