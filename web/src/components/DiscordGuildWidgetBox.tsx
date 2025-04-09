import {DiscordGuildWidget} from "../lib/api/dtos.ts";
import Stack from "@mui/material/Stack/Stack";
import Typography from "@mui/material/Typography/Typography";
import Grid from "@mui/material/Grid/Grid";
import Button from "@mui/material/Button/Button";
import Link from "@mui/material/Link";
import Box from "@mui/material/Box/Box";
import GroupsIcon from '@mui/icons-material/Groups';
import Avatar from "@mui/material/Avatar/Avatar";
import Alert from "@mui/material/Alert/Alert";

interface DiscordGuildWidgetProps {
    discordGuildWidget: DiscordGuildWidget | null;
    discordGuildWidgetLoadingError: string | null;
}

const DiscordGuildWidgetBox = (props: DiscordGuildWidgetProps) => {
    return (
        <>
            {props.discordGuildWidgetLoadingError && (
                <Alert severity="error" variant="filled">Failed to load discord guild widget: {props.discordGuildWidgetLoadingError}</Alert>
            )}
            {!props.discordGuildWidget && !props.discordGuildWidgetLoadingError && (
                <Alert severity="info" variant="filled">Loading discord guild widget ...</Alert>
            )}
            {!props.discordGuildWidgetLoadingError && props.discordGuildWidget && (
                <Stack spacing={2}>
                    <Box>
                        <Typography variant={"h5"}>Discord - {props.discordGuildWidget.name}</Typography>
                        <Typography variant={"body1"}>{props.discordGuildWidget.member_count} members online</Typography>
                    </Box>

                    <Grid container>
                        {props.discordGuildWidget.members.map((member) => (
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

                    <Link href={props.discordGuildWidget.invite_link}>
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

export default DiscordGuildWidgetBox;