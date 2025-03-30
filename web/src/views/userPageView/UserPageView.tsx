import {Alert, Avatar, List, ListItem, ListItemAvatar, ListItemText, Stack, Typography} from "@mui/material";
import {useEffect, useState} from "react";
import {useSearchParams} from "react-router-dom";
import PersonIcon from '@mui/icons-material/Person';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import formatDate from "../../utils/formatDate.ts";
import ApiClient from "../../lib/services/apiClient.ts";
import {CustomTrack} from "../../lib/api/dtos.ts";
import randomSlice from "../../utils/randomSlice.ts";
import CustomTrackListGrid from "../../components/CustomTrackListGrid.tsx";
import ServiceManager from "../../lib/serviceManager.ts";

const UserPageView = () => {
    const apiClient: ApiClient = ServiceManager.createApiClient();

    const [searchParams] = useSearchParams();
    const [user, setUser] = useState<any>(null);
    const [userCustomTracks, setUserCustomTracks] = useState<CustomTrack[]>([]);

    useEffect(() => {
        const id = Number(searchParams.get('id'));
        apiClient.findUsers(id, null, null, null, null).then(query => setUser(query.items[0]));
    }, [searchParams, setUser]);

    useEffect(() => {
        if (user) {
            apiClient.findCustomTracks(null, user.id, null, null, null, 1, 50).then((query) => {
                const randomTracks: CustomTrack[] = randomSlice(query.items, 6);
                setUserCustomTracks(randomTracks)
            });
        }
    }, [user, setUserCustomTracks]);

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
                            <Alert severity="info" variant="filled">This listing shows a random selection of 6 custom tracks created by {user.username}.</Alert>
                            <CustomTrackListGrid customTracks={userCustomTracks}/>
                        </Stack>
                    )}
                </>
            )}
            {!user && <Alert severity="warning" variant="filled">No player found.</Alert>}
        </>
    );
}

export default UserPageView;