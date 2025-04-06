import ApiClient from "../lib/services/apiClient.ts";
import ServiceManager from "../lib/serviceManager.ts";
import {useEffect, useState} from "react";
import {DiscordGuildWidget} from "../lib/api/dtos.ts";
import Stack from "@mui/material/Stack/Stack";
import Alert from "@mui/material/Alert/Alert";
import Typography from "@mui/material/Typography/Typography";
import Grid from "@mui/material/Grid/Grid";
import Button from "@mui/material/Button/Button";
import Link from "@mui/material/Link";
import Box from "@mui/material/Box/Box";
import GroupsIcon from '@mui/icons-material/Groups';
import Avatar from "@mui/material/Avatar/Avatar";

const DiscordWidget = () => {
    const apiClient: ApiClient = ServiceManager.createApiClient();

    const [discordGuildWidget, setDiscordGuildWidget] = useState<DiscordGuildWidget | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        apiClient.getDiscordStatus().then((status) => {
            if (status.success) {
                setDiscordGuildWidget(status.widget);
            } else {
                setError(status.error);
            }
        });
    }, []);

    return (
        <>
            {error && (
                <Alert severity="error" variant="filled">Failed to load discord guild widget: {error}</Alert>
            )}
            {!discordGuildWidget && !error && (
                <Alert severity="info" variant="filled">Loading discord guild widget ...</Alert>
            )}
            {!error && discordGuildWidget && (
                <Stack spacing={2}>
                    <Box>
                        <Typography variant={"h5"}>Discord - {discordGuildWidget.name}</Typography>
                        <Typography variant={"body1"}>{discordGuildWidget.member_count} members online</Typography>
                    </Box>

                    <Grid container>
                        {discordGuildWidget.members.map((member) => (
                            <Grid container spacing={1} sx={{ mb: 0.5 }} key={member.id}>
                                <Grid item>
                                    <Avatar
                                        alt={member.username}
                                        src={member.avatar}
                                        sx={{width: 25, height: 25}}
                                    />
                                </Grid>
                                <Grid item>
                                    <Typography variant="body1">{member.username}</Typography>
                                </Grid>
                            </Grid>
                        ))}
                    </Grid>

                    <Link href={discordGuildWidget.invite_link}>
                        <Button variant={"contained"}>
                            <GroupsIcon sx={{mr: 1}}/>
                            Join the discord
                        </Button>
                    </Link>
                </Stack>
            )}
        </>
    )
}

export default DiscordWidget;