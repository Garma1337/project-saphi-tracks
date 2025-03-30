import {Box, Card, CardContent, CardMedia, Chip, Link, Typography} from "@mui/material";
import AppRoutes from "../routes.tsx";
import formatDate from "../utils/formatDate.ts";
import {useNavigate} from "react-router-dom";
import {CustomTrack, Resource} from "../lib/api/dtos.ts";
import ApiClient from "../lib/services/apiClient.ts";
import ServiceManager from "../lib/serviceManager.ts";

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
                        <CardMedia
                            component="img"
                            height="250"
                            image={apiClient.proxyResource(getPreviewImage(customTrack))}
                            alt={customTrack.name}
                        />
                        <Box>
                            <h2>
                                <Link onClick={() => navigate(AppRoutes.CustomTrackDetailPage + "?id=" + customTrack.id)}>
                                    {customTrack.name}
                                </Link>
                                <Chip
                                    size={'small'}
                                    label={customTrack.verified ? 'Verified' : 'Unverified'}
                                    color={customTrack.verified ? 'success' : 'error'}
                                    sx={{ml: 1}}
                                />
                            </h2>
                            <Typography>
                                Author: <Link
                                onClick={() => navigate(AppRoutes.UserDetailPage + "?id=" + customTrack.author_id)}>{customTrack.author.username}</Link>
                            </Typography>
                            <Typography>
                                Created: {formatDate(customTrack.created.toLocaleString())}
                            </Typography>
                        </Box>
                    </CardContent>
                </Card>
            ))}
        </Box>
    )
}

export default CustomTrackListGrid;