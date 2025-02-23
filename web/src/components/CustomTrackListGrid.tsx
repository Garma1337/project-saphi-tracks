import {Box, Button, Card, CardContent, CardMedia, Link, Typography} from "@mui/material";
import AppRoutes from "../routes.tsx";
import formatDate from "../utils/formatDate.ts";
import ZoomInIcon from "@mui/icons-material/ZoomIn";
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
                            height="125"
                            image={"https://ctrcustomtracks.com/wp-content/uploads/2025/01/NeonParadise-300x222.png"}
                            alt={customTrack.name}
                        />
                        <Box>
                            <h2>{customTrack.name}</h2>
                            <Typography>
                                By: <Link
                                onClick={() => navigate(AppRoutes.UserDetailPage + "?id=" + customTrack.author_id)}>{customTrack.author.username}</Link>
                            </Typography>
                            <Typography>
                                Created: {formatDate(customTrack.created.toLocaleString())}
                            </Typography>
                            <Button
                                variant="outlined"
                                onClick={() => navigate(AppRoutes.CustomTrackDetailPage + "?id=" + customTrack.id)}
                            >
                                <ZoomInIcon sx={{marginRight: 1}}/>
                                Details
                            </Button>
                        </Box>
                    </CardContent>
                </Card>
            ))}
        </Box>
    )
}

export default CustomTrackListGrid;