import {
    AppBar,
    Box,
    Button,
    Container,
    Drawer,
    IconButton,
    Menu,
    MenuItem,
    Stack,
    Toolbar,
    useMediaQuery,
    useTheme
} from "@mui/material"
import {Outlet, useNavigate} from "react-router-dom";
import AppRoutes from "../../routes.tsx";
import useStore from "../../store.ts";
import Brightness4Icon from '@mui/icons-material/Brightness4';
import {AccountCircle, Menu as MenuIcon} from "@mui/icons-material";
import React, {useState} from "react";
import HomeIcon from '@mui/icons-material/Home';
import PeopleIcon from '@mui/icons-material/People';
import CollectionsIcon from '@mui/icons-material/Collections';
import PaletteIcon from '@mui/icons-material/Palette';
import BuildIcon from '@mui/icons-material/Build';
import AutoStoriesIcon from '@mui/icons-material/AutoStories';
import SettingsIcon from '@mui/icons-material/Settings';
import ServiceManager from "../../lib/serviceManager.ts";
import toggleTheme from "../../utils/toggleTheme.ts";

const Layout = () => {
    const sessionManager = ServiceManager.createSessionManager();

    const navigate = useNavigate();
    const currentUser = useStore(state => state.currentUser);
    const displayOptions = useStore(state => state.displayOptions);
    const [accountAnchorEL, setAccountAnchorEL] = React.useState<null | HTMLElement>(null);
    const [drawerOpen, setDrawerOpen] = useState(false);

    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('md'));

    const handleAccountMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAccountAnchorEL(event.currentTarget);
    };

    const handleAccountMenuClose = () => {
        setAccountAnchorEL(null);
    };

    const logoutPlayer = () => {
        sessionManager.logout().then(() => {
            window.location.reload();
        });
    }

    const handleDrawerToggle = () => {
        setDrawerOpen(!drawerOpen);
    };

    const drawer = (
        <Box onClick={handleDrawerToggle}>
            <Stack spacing={2} sx={{padding: 2 }}>
                <Button color="inherit" onClick={() => navigate(AppRoutes.IndexPage)} sx={{ justifyContent: 'flex-start'}}>
                    <HomeIcon sx={{marginRight: 1}}/>
                    Home
                </Button>
                <Button color="inherit" onClick={() => navigate(AppRoutes.CustomTrackListPage)} sx={{ justifyContent: 'flex-start'}}>
                    <CollectionsIcon sx={{marginRight: 1}}/>
                    Custom Tracks
                </Button>
                <Button color="inherit" onClick={() => navigate(AppRoutes.ToolsPage)} sx={{ justifyContent: 'flex-start'}}>
                    <BuildIcon sx={{marginRight: 1}}/>
                    Tools
                </Button>
                <Button color="inherit" onClick={() => navigate(AppRoutes.TutorialPage)} sx={{ justifyContent: 'flex-start'}}>
                    <AutoStoriesIcon sx={{marginRight: 1}}/>
                    Tutorial
                </Button>
                <Button color="inherit" onClick={() => navigate(AppRoutes.UserListPage)} sx={{ justifyContent: 'flex-start'}}>
                    <PeopleIcon sx={{marginRight: 1}}/>
                    Users
                </Button>
                {displayOptions?.get('show_admin_button') && (
                    <Button color="inherit" onClick={() => navigate(AppRoutes.AdminPage)} sx={{ justifyContent: 'flex-start'}}>
                        <SettingsIcon sx={{marginRight: 1}}/>
                        Admin
                    </Button>
                )}
            </Stack>
        </Box>
    );

    return (
        <Box sx={{flexGrow: 1}}>
            <AppBar position="static" color="primary" enableColorOnDark>
                <Container>
                    <Toolbar>
                        <IconButton
                            size="large"
                            edge="start"
                            color="inherit"
                            aria-label="menu"
                            onClick={handleDrawerToggle}
                        >
                            {isMobile ? <MenuIcon/> : <PaletteIcon/>}
                        </IconButton>
                        {!isMobile && (
                            <Box sx={{flexGrow: 1}}>
                                <Button color="inherit" onClick={() => navigate(AppRoutes.IndexPage)}>
                                    <HomeIcon sx={{marginRight: 1}}/>
                                    Home
                                </Button>
                                <Button color="inherit" onClick={() => navigate(AppRoutes.CustomTrackListPage)}>
                                    <CollectionsIcon sx={{marginRight: 1}}/>
                                    Custom Tracks
                                </Button>
                                <Button color="inherit" onClick={() => navigate(AppRoutes.ToolsPage)}>
                                    <BuildIcon sx={{marginRight: 1}}/>
                                    Tools
                                </Button>
                                <Button color="inherit" onClick={() => navigate(AppRoutes.TutorialPage)}>
                                    <AutoStoriesIcon sx={{marginRight: 1}}/>
                                    Tutorial
                                </Button>
                                <Button color="inherit" onClick={() => navigate(AppRoutes.UserListPage)}>
                                    <PeopleIcon sx={{marginRight: 1}}/>
                                    Users
                                </Button>
                                {displayOptions?.get('show_admin_button') && (
                                    <Button color="inherit" onClick={() => navigate(AppRoutes.AdminPage)}>
                                        <SettingsIcon sx={{marginRight: 1}}/>
                                        Admin
                                    </Button>
                                )}
                            </Box>
                        )}
                        {displayOptions.get('show_login_button') && (
                            <Button color="inherit" onClick={() => navigate(AppRoutes.LoginPage)}>Login</Button>
                        )}
                        {currentUser && (
                            <div>
                                <Button onClick={handleAccountMenu} color="inherit">
                                    <AccountCircle sx={{marginRight: 1}}/>
                                    {currentUser.username}
                                </Button>
                                <Menu
                                    id="menu-appbar"
                                    anchorEl={accountAnchorEL}
                                    anchorOrigin={{
                                        vertical: 'top',
                                        horizontal: 'right',
                                    }}
                                    keepMounted
                                    transformOrigin={{
                                        vertical: 'top',
                                        horizontal: 'right',
                                    }}
                                    open={Boolean(accountAnchorEL)}
                                    onClose={handleAccountMenuClose}
                                >
                                    <MenuItem
                                        onClick={() => navigate(AppRoutes.UserDetailPage + '?id=' + currentUser.id)}>Profile</MenuItem>
                                    <MenuItem onClick={() => logoutPlayer()}>Logout</MenuItem>
                                </Menu>
                            </div>
                        )}
                        <IconButton
                            size="large"
                            edge="end"
                            color="inherit"
                            aria-label="toggle theme"
                            onClick={toggleTheme}
                        >
                            <Brightness4Icon/>
                        </IconButton>
                    </Toolbar>
                </Container>
            </AppBar>
            <Drawer
                anchor="left"
                open={drawerOpen}
                onClose={handleDrawerToggle}
            >
                {drawer}
            </Drawer>
            <Container sx={{my: 2 }}>
                <Outlet/>
            </Container>
        </Box>
    );
}

export default Layout;