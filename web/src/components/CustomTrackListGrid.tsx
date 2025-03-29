import {Box, Card, CardContent, CardMedia, Chip, Link, Typography} from "@mui/material";
import AppRoutes from "../routes.tsx";
import formatDate from "../utils/formatDate.ts";
import {useNavigate} from "react-router-dom";
import {CustomTrack} from "../lib/api/dtos.ts";

interface CustomTrackListGridProps {
    customTracks: CustomTrack[]
}

const CustomTrackListGrid = (props: CustomTrackListGridProps) => {
    const navigate = useNavigate();

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
                            image={"https://ctrcustomtracks.com/wp-content/uploads/2025/01/NeonParadise-300x222.png"}
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