import Stack from "@mui/material/Stack/Stack";
import Typography from "@mui/material/Typography/Typography";
import ApiClient from "../../lib/services/apiClient.ts";
import ServiceManager from "../../lib/serviceManager.ts";
import {useEffect, useState} from "react";
import {CustomTrack, Resource} from "../../lib/api/dtos.ts";
import {useSearchParams} from "react-router-dom";
import Alert from "@mui/material/Alert/Alert";
import Accordion from "@mui/material/Accordion/Accordion";
import AccordionDetails from "@mui/material/AccordionDetails/AccordionDetails";
import AccordionSummary from "@mui/material/AccordionSummary/AccordionSummary";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import YouTubeVideo from "../../components/YouTubeVideo.tsx";
import DownloadResourceLink from "../../components/ResourceDownloadButton.tsx";
import Blockquote from "../../components/BlockQuote.tsx";

const CustomTrackPageView = () => {
    const apiClient: ApiClient = ServiceManager.createApiClient();

    const [searchParams] = useSearchParams();
    const [customTrack, setCustomTrack] = useState<CustomTrack | null>(null);
    const [resources, setResources] = useState<Resource[]>([]);

    useEffect(() => {
        const id = Number(searchParams.get('id'));
        apiClient.findCustomTracks(id, null, null, null, null, null, null).then((query) => {
            setCustomTrack(query.items[0]);
        });
    }, [searchParams, setCustomTrack]);

    useEffect(() => {
        if (customTrack) {
            setResources(customTrack.resources.filter((resource) => resource.resource_type !== 'preview'));
        }
    }, [customTrack, setResources]);

    return (
        <Stack spacing={2}>
            {customTrack && (
                <>
                    <Typography variant="h4">{customTrack.name}</Typography>

                    {!customTrack.verified && (
                        <Alert severity="warning">This track has not been verified yet.</Alert>
                    )}

                    <YouTubeVideo src={customTrack.video}/>

                    <Typography>
                        Here is what {customTrack.author.username} has to say about the track:
                    </Typography>
                    <Blockquote text={customTrack.description}/>

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
                                {resources.map((resource) => (
                                    <li>
                                        <DownloadResourceLink resourceId={resource.id} label={resource.file_name} /> (v{resource.version})
                                    </li>
                                ))}
                            </ul>
                        </AccordionDetails>
                    </Accordion>
                </>
            )}
            {!customTrack && <Alert severity="warning">No custom track found.</Alert>}
        </Stack>
    );
}

export default CustomTrackPageView;