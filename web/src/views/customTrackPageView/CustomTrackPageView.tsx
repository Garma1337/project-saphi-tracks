import Stack from "@mui/material/Stack/Stack";
import Typography from "@mui/material/Typography/Typography";
import ApiClient from "../../lib/services/apiClient.ts";
import ServiceManager from "../../lib/serviceManager.ts";
import {useEffect, useState} from "react";
import {CustomTrack, Resource} from "../../lib/api/dtos.ts";
import {useNavigate, useSearchParams} from "react-router-dom";
import Alert from "@mui/material/Alert/Alert";
import Accordion from "@mui/material/Accordion/Accordion";
import AccordionDetails from "@mui/material/AccordionDetails/AccordionDetails";
import AccordionSummary from "@mui/material/AccordionSummary/AccordionSummary";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import YouTubeVideo from "../../components/YouTubeVideo.tsx";
import Blockquote from "../../components/BlockQuote.tsx";
import Button from "@mui/material/Button/Button";
import Grid from "@mui/material/Grid/Grid";
import randomSlice from "../../utils/randomSlice.ts";
import CustomTrackListGrid from "../../components/CustomTrackListGrid.tsx";
import SimpleDialog from "../../components/SimpleDialog.tsx";
import AppRoutes from "../../routes.tsx";
import Menu from "@mui/material/Menu/Menu";
import MenuItem from "@mui/material/MenuItem/MenuItem";
import useStore from "../../store.ts";
import FormatListBulletedIcon from '@mui/icons-material/FormatListBulleted';
import DeleteIcon from '@mui/icons-material/Delete';
import CheckIcon from '@mui/icons-material/Check';
import ResourceListTable from "../../components/ResourceListTable.tsx";

const CustomTrackPageView = () => {
    const apiClient: ApiClient = ServiceManager.createApiClient();
    const navigate = useNavigate();
    const displayOptions = useStore(state => state.displayOptions);

    const [searchParams] = useSearchParams();
    const [customTrack, setCustomTrack] = useState<CustomTrack | null>(null);
    const [userCustomTracks, setUserCustomTracks] = useState<CustomTrack[]>([]);
    const [resources, setResources] = useState<Resource[]>([]);
    const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
    const [verifyModalOpen, setVerifyModalOpen] = useState(false);
    const [verifySuccess, setVerifySuccess] = useState<boolean | null>(null);
    const [verifyError, setVerifyError] = useState<string | null>(null);
    const [deleteModalOpen, setDeleteModalOpen] = useState(false);
    const [deleteError, setDeleteError] = useState<string | null>(null);

    const menuOpen = Boolean(anchorEl);

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

        setVerifyModalOpen(false);
    }

    const deleteCustomTrack = async (customTrack: CustomTrack) => {
        setDeleteError(null);

        const response = await apiClient.deleteCustomTrack(customTrack.id);
        if (response.success) {
            navigate(AppRoutes.IndexPage);
        } else {
            setDeleteError(response.error);
        }

        setDeleteModalOpen(false);
    }

    const openVerifyModal = () => {
        setVerifyModalOpen(true);
        handleMenuClose();
    }

    const openDeleteModal = () => {
        setDeleteModalOpen(true);
        handleMenuClose();
    }

    const handleMenuClick = (event: React.MouseEvent<HTMLButtonElement>) => {
        setAnchorEl(event.currentTarget);
    }

    const handleMenuClose = () => {
        setAnchorEl(null);
    }

    return (
        <Stack spacing={2}>
            {customTrack && (
                <>
                    <Grid container>
                        <Typography variant="h4">{customTrack.name}</Typography>

                        {displayOptions?.get('show_admin_button') && (
                            <>
                                <Button
                                    id="basic-button"
                                    variant="contained"
                                    color="primary"
                                    aria-controls={menuOpen ? 'basic-menu' : undefined}
                                    aria-haspopup="true"
                                    aria-expanded={menuOpen ? 'true' : undefined}
                                    onClick={handleMenuClick}
                                    sx={{marginLeft: 'auto'}}
                                >
                                    <FormatListBulletedIcon sx={{ mr: 1 }} />
                                    Moderator Actions
                                </Button>
                                <Menu
                                    id="basic-menu"
                                    anchorEl={anchorEl}
                                    open={menuOpen}
                                    onClose={handleMenuClose}
                                    MenuListProps={{
                                        'aria-labelledby': 'basic-button',
                                    }}
                                >
                                    {!customTrack.verified && displayOptions?.get('show_verify_custom_track_button') && (
                                        <MenuItem onClick={() => openVerifyModal()}>
                                            <CheckIcon sx={{ mr: 1 }} />
                                            Verify Custom Track
                                        </MenuItem>
                                    )}

                                    {displayOptions?.get('show_delete_custom_track_button') && (
                                        <MenuItem onClick={() => openDeleteModal()}>
                                            <DeleteIcon sx={{ mr: 1 }} />
                                            Delete Custom Track
                                        </MenuItem>
                                    )}
                                </Menu>
                            </>
                        )}
                    </Grid>

                    {deleteError && <Alert severity="error" variant="filled">{deleteError}</Alert>}

                    {!customTrack.verified && (
                        <>
                            {verifyError && <Alert severity="error" variant="filled">{verifyError}</Alert>}
                            <Alert severity="warning" variant="filled">This track has not been verified yet, so it can only be seen by moderators.</Alert>
                        </>
                    )}

                    {verifySuccess && <Alert severity="success" variant="filled">The track has been verified successfully!</Alert>}

                    <Accordion>
                        <AccordionSummary
                            expandIcon={<ExpandMoreIcon/>}
                            aria-controls="panel1-content"
                            id="panel1-header"
                        >
                            <Typography component="span">Downloads</Typography>
                        </AccordionSummary>
                        <AccordionDetails>
                            <ResourceListTable resources={resources} borderLess={true} />
                        </AccordionDetails>
                    </Accordion>

                    <YouTubeVideo src={customTrack.video}/>

                    <Typography>
                        {customTrack.author.username} says:
                    </Typography>
                    <Blockquote text={customTrack.description}/>

                    <SimpleDialog
                        open={verifyModalOpen}
                        onClose={() => setVerifyModalOpen(false)}
                        title={`Verify custom track "${customTrack.name}"?`}
                        description={"This action cannot be undone. The track will be visible to all users and can be downloaded ingame."}
                        actions={
                            <>
                                <Button onClick={() => setVerifyModalOpen(false)} variant="outlined" color="inherit">Back</Button>
                                <Button onClick={() => verifyCustomTrack(customTrack)} variant="contained" color="success" autoFocus>
                                    Verify
                                </Button>
                            </>
                        }
                    />

                    <SimpleDialog
                        open={deleteModalOpen}
                        onClose={() => setDeleteModalOpen(false)}
                        title={`Delete custom track "${customTrack.name}"?`}
                        description={"This action cannot be undone. The track, including all resources, will be removed immediately."}
                        actions={
                            <>
                                <Button onClick={() => setDeleteModalOpen(false)} variant="outlined" color="inherit">Back</Button>
                                <Button onClick={() => deleteCustomTrack(customTrack)} variant="contained" color="error" autoFocus>
                                    Delete
                                </Button>
                            </>
                        }
                    />

                    {userCustomTracks.length > 0 && (
                        <>
                            <Typography variant="h4">Other Custom Tracks by {customTrack.author.username}</Typography>
                            <CustomTrackListGrid customTracks={userCustomTracks}/>
                        </>
                    )}
                </>
            )}
            {!customTrack && <Alert severity="warning" variant="filled">No custom track found.</Alert>}
        </Stack>
    );
}

export default CustomTrackPageView;