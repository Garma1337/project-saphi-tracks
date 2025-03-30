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
import Button from "@mui/material/Button/Button";
import Grid from "@mui/material/Grid/Grid";
import Dialog from "@mui/material/Dialog/Dialog";
import DialogTitle from "@mui/material/DialogTitle/DialogTitle";
import DialogContent from "@mui/material/DialogContent/DialogContent";
import DialogContentText from "@mui/material/DialogContentText/DialogContentText";
import DialogActions from "@mui/material/DialogActions/DialogActions";
import randomSlice from "../../utils/randomSlice.ts";
import CustomTrackListGrid from "../../components/CustomTrackListGrid.tsx";

const CustomTrackPageView = () => {
    const apiClient: ApiClient = ServiceManager.createApiClient();

    const [searchParams] = useSearchParams();
    const [customTrack, setCustomTrack] = useState<CustomTrack | null>(null);
    const [userCustomTracks, setUserCustomTracks] = useState<CustomTrack[]>([]);
    const [resources, setResources] = useState<Resource[]>([]);
    const [verifyModalOpen, setVerifyModalOpen] = useState(false);
    const [verifySuccess, setVerifySuccess] = useState<boolean | null>(null);
    const [verifyError, setVerifyError] = useState<string | null>(null);

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

    useEffect(() => {
        if (customTrack) {
            apiClient.findCustomTracks(null, customTrack.author.id, null, null, null, 1, 50).then((query) => {
                const randomTracks: CustomTrack[] = randomSlice(query.items, 6);
                setUserCustomTracks(randomTracks)
            });
        }
    }, [customTrack, setUserCustomTracks]);

    const verifyCustomTrack = async (customTrack: CustomTrack) => {
        setVerifyError(null);

        const response = await apiClient.verifyCustomTrack(customTrack.id);
        if (response.success) {
            setCustomTrack({...customTrack, verified: true});
            setVerifySuccess(true);
        } else {
            setVerifyError(response.error);
        }

        closeModal();
    }

    const openModal = () => {
        setVerifyModalOpen(true);
    }

    const closeModal = () => {
        setVerifyModalOpen(false);
    }

    return (
        <Stack spacing={2}>
            {customTrack && (
                <>
                    <Grid container>
                        <Grid item xs={10}>
                            <Typography variant="h4">{customTrack.name}</Typography>
                        </Grid>
                        <Grid item xs={2}>
                            {!customTrack.verified && (
                                <Button
                                    variant="contained"
                                    color="success"
                                    onClick={openModal}
                                >
                                    Verify this track
                                </Button>
                            )}
                        </Grid>
                    </Grid>

                    {!customTrack.verified && (
                        <>
                            {verifyError && <Alert severity="error">{verifyError}</Alert>}
                            <Alert severity="warning">This track has not been verified yet, so it can only be seen by moderators.</Alert>
                        </>
                    )}

                    {verifySuccess && <Alert severity="success">The track has been verified successfully!</Alert>}

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

                    <YouTubeVideo src={customTrack.video}/>

                    <Typography>
                        {customTrack.author.username} says:
                    </Typography>
                    <Blockquote text={customTrack.description}/>

                    <Dialog
                        open={verifyModalOpen}
                        onClose={openModal}
                        aria-labelledby="alert-dialog-title"
                        aria-describedby="alert-dialog-description"
                    >
                        <DialogTitle id="alert-dialog-title">
                            Verify custom track "{customTrack.name}"?
                        </DialogTitle>
                        <DialogContent>
                            <DialogContentText id="alert-dialog-description">
                                This action cannot be undone. The track will be visible to all users
                                and can be downloaded ingame.
                            </DialogContentText>
                        </DialogContent>
                        <DialogActions>
                            <Button onClick={closeModal} variant={"outlined"}>Back</Button>
                            <Button onClick={() => verifyCustomTrack(customTrack)} variant={"contained"} color={"success"} autoFocus>
                                Verify
                            </Button>
                        </DialogActions>
                    </Dialog>

                    {userCustomTracks.length > 0 && (
                        <>
                            <Typography variant="h4">Custom tracks made by {customTrack.author.username} ...</Typography>
                            <CustomTrackListGrid customTracks={userCustomTracks}/>
                        </>
                    )}
                </>
            )}
            {!customTrack && <Alert severity="warning">No custom track found.</Alert>}
        </Stack>
    );
}

export default CustomTrackPageView;