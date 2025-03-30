import {Alert, Box, Link, Typography} from "@mui/material";

const ToolsView = () => {
    return (
        <>
            <Typography variant="h4">Tools</Typography>

            <Box my={2}>
                <Alert severity="info" variant="filled">
                    In this section you can find tools which you need to create, modify or play CTR with custom tracks. Depending on what you are planning to do,
                    you will not need all of them. If you are not sure what you need, you can ask for help in our <Link href={"https://discord.gg/6mxqGJmkKJ"}>Discord server</Link>.
                </Alert>
            </Box>

            <ul>
                <li>
                    <Link href={"https://www.duckstation.org/"}>Duckstation</Link> - The only supported PS1 emulator for Project Saphi
                </li>
                <li>
                    <Link href={"https://www.blender.org/"}>Blender</Link> - A 3D modeling software
                </li>
                <li>
                    <Link href={"https://github.com/mateusfavarin/CrashTeamEditor"}>Crash Team Editor</Link> - A tool to create CTR tracks from a 3D model
                </li>
                <li>
                    <Link href={"https://github.com/CTR-tools/CTR-tools"}>CTR Tools</Link> - A collection of tools to parse files from the original CTR
                </li>
                <li>
                    <Link href={"https://github.com/CTR-tools/CTR-ModSDK"}>CTR Mod SDK</Link> - A modding toolkit specifically for CTR
                </li>
                <li>
                    <Link href={"https://github.com/mateusfavarin/psx-modding-toolchain"}>PSX Modding Toolchain</Link> - A collection of tools to mod PS1 games
                </li>
            </ul>
        </>
    );
}

export default ToolsView;