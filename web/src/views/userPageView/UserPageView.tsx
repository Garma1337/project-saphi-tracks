import {Alert, Avatar, List, ListItem, ListItemAvatar, ListItemText, Stack, Typography} from "@mui/material";
import {useSearchParams} from "react-router-dom";
import PersonIcon from '@mui/icons-material/Person';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import formatDate from "../../utils/formatDate.ts";
import ApiClient from "../../lib/services/apiClient.ts";
import CustomTrackListGrid from "../../components/CustomTrackListGrid.tsx";
import ServiceManager from "../../lib/serviceManager.ts";
import useUserPageViewModel from "../../viewModels/useUserPageViewModel.ts";

const UserPageView = () => {
    const apiClient: ApiClient = ServiceManager.createApiClient();

    const [searchParams] = useSearchParams();

    const { user, userCustomTracks } = useUserPageViewModel(
        apiClient,
        searchParams,
    )

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