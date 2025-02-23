import {Alert, Avatar, List, ListItem, ListItemAvatar, ListItemText, Stack, Typography} from "@mui/material";
import {useEffect, useState} from "react";
import {useSearchParams} from "react-router-dom";
import PersonIcon from '@mui/icons-material/Person';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import formatDate from "../../utils/formatDate.ts";
import ApiClient from "../../lib/apiClient.ts";
import {CustomTrack} from "../../lib/api/dtos.ts";
import randomSlice from "../../utils/randomSlice.ts";
import CustomTrackListGrid from "../../components/CustomTrackListGrid.tsx";

const UserPageView = () => {
    const [searchParams] = useSearchParams();
    const [apiClient, setApiClient] = useState<ApiClient | null>(null);
    const [user, setUser] = useState<any>(null);
    const [userCustomTracks, setUserCustomTracks] = useState<CustomTrack[]>([]);

    useEffect(() => {
        if (apiClient) {
            const id = Number(searchParams.get('id'));
            apiClient.findUsers(id, null, null, null, null).then(query => setUser(query.items[0]));
        }
    }, [apiClient, searchParams, setUser]);

    useEffect(() => {
        if (apiClient && user) {
            apiClient.findCustomTracks(null, user.id, null, null, null, 1, 50).then((query) => {
                const randomTracks: CustomTrack[] = randomSlice(query.items, 6);
                setUserCustomTracks(randomTracks)
            });
        }
    }, [apiClient, user, setUserCustomTracks]);

    useEffect(() => {
        setApiClient(new ApiClient('http://localhost:5000/api/v1'));
    }, []);

    return (
        <>
            {user && (
                <>
                    <Typography variant="h4">User Profile</Typography>

                    <List sx={{width: '100%', maxWidth: 360, bgcolor: 'background.paper'}}>
                        <ListItem>
                            <ListItemAvatar>
                                <Avatar>
                                    <PersonIcon/>
                                </Avatar>
                            </ListItemAvatar>
                            <ListItemText primary="Name" secondary={user.username}/>
                        </ListItem>
                        <ListItem>
                            <ListItemAvatar>
                                <Avatar>
                                    <AccessTimeIcon/>
                                </Avatar>
                            </ListItemAvatar>
                            <ListItemText primary="Registered since" secondary={formatDate(user.created)}/>
                        </ListItem>
                    </List>

                    {userCustomTracks.length > 0 && (
                        <Stack spacing={2}>
                            <Typography variant="h4">Custom Tracks</Typography>
                            <Alert severity={"info"}>This listing shows a random selection of 6 custom tracks created by {user.username}.</Alert>
                            <CustomTrackListGrid customTracks={userCustomTracks}/>
                        </Stack>
                    )}
                </>
            )}
            {!user && <Alert severity="warning">No player found.</Alert>}
        </>
    );
}

export default UserPageView;