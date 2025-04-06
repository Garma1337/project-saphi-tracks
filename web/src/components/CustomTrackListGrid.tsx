import {Box, Button, Card, CardContent, CardMedia, Chip, Link, Stack, Typography} from "@mui/material";
import AppRoutes from "../routes.tsx";
import formatDate from "../utils/formatDate.ts";
import {useNavigate} from "react-router-dom";
import {CustomTrack, Resource} from "../lib/api/dtos.ts";
import ApiClient from "../lib/services/apiClient.ts";
import ServiceManager from "../lib/serviceManager.ts";
import DownloadIcon from '@mui/icons-material/Download';

interface CustomTrackListGridProps {
    customTracks: CustomTrack[]
}

const CustomTrackListGrid = (props: CustomTrackListGridProps) => {
    const apiClient: ApiClient = ServiceManager.createApiClient();
    const navigate = useNavigate();

    const getPreviewImage = (customTrack: CustomTrack): Resource | null => {
        return customTrack.resources.find(resource => resource.resource_type === 'preview') || null;
    }

    return (
        <Box sx={{
            width: "100%",
            display: "grid",
            gap: 2,
            gridTemplateColumns: 'repeat(auto-fill, minmax(min(300px, 100%), 1fr))'
        }}>
            {props.customTracks.map(customTrack => (
                <Card>
                    <CardContent>
                        <Stack spacing={2}>
                            <CardMedia
                                component="img"
                                height="250"
                                image={apiClient.proxyResource(getPreviewImage(customTrack))}
                                alt={customTrack.name}
                            />
                            <Box>
                                <Typography variant="h5">
                                    {customTrack.name}
                                    <Chip
                                        size={'small'}
                                        label={customTrack.verified ? 'Verified' : 'Unverified'}
                                        color={customTrack.verified ? 'success' : 'error'}
                                        sx={{ml: 1}}
                                    />
                                </Typography>
                            </Box>
                            <Box>
                                <Typography>
                                    Author: <Link
                                    onClick={() => navigate(AppRoutes.UserDetailPage + "?id=" + customTrack.author_id)}>{customTrack.author.username}</Link>
                                </Typography>
                                <Typography>
                                    Created: {formatDate(customTrack.created.toLocaleString())}
                                </Typography>
                            </Box>
                            <Button variant="contained" onClick={() => navigate(AppRoutes.CustomTrackDetailPage + "?id=" + customTrack.id)}>
                                <DownloadIcon sx={{mr: 1}}/>
                                Download
                            </Button>
                        </Stack>
                    </CardContent>
                </Card>
            ))}
        </Box>
    )
}

export default CustomTrackListGrid;