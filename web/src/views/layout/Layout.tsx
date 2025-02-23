import {AppBar, Box, Button, Container, IconButton, Menu, MenuItem, Toolbar} from "@mui/material"
import {Outlet, useNavigate} from "react-router-dom";
import AppRoutes from "../../routes.tsx";
import useStore from "../../store.ts";
import Brightness4Icon from '@mui/icons-material/Brightness4';
import {AccountCircle} from "@mui/icons-material";
import React from "react";
import HomeIcon from '@mui/icons-material/Home';
import PeopleIcon from '@mui/icons-material/People';
import CollectionsIcon from '@mui/icons-material/Collections';
import PaletteIcon from '@mui/icons-material/Palette';
import BuildIcon from '@mui/icons-material/Build';
import AutoStoriesIcon from '@mui/icons-material/AutoStories';

const Layout = () => {
    const navigate = useNavigate();
    const setJwt = useStore(state => state.setJwt);
    const currentUser = useStore(state => state.currentUser);
    const setCurrentUser = useStore(state => state.setCurrentUser);
    const [accountAnchorEL, setAccountAnchorEL] = React.useState<null | HTMLElement>(null);

    const handleAccountMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAccountAnchorEL(event.currentTarget);
    };

    const handleAccountMenuClose = () => {
        setAccountAnchorEL(null);
    };

    const logoutPlayer = () => {
        localStorage.removeItem('jwt');
        setJwt('');
        setCurrentUser(null);
        navigate(AppRoutes.IndexPage);
    }

    const toggleTheme = () => {
        const newTheme = localStorage.getItem('theme') === 'light' ? 'dark' : 'light';
        localStorage.setItem('theme', newTheme);
        window.location.reload();
    }

    return (
        <Box sx={{flexGrow: 1}}>
            <AppBar position="static">
                <Container>
                    <Toolbar sx={{paddingLeft: 0, paddingRight: 0}}>
                        <IconButton
                            size="large"
                            edge="start"
                            color="inherit"
                            aria-label="menu"
                            sx={{mr: 2}}
                        >
                            <PaletteIcon/>
                        </IconButton>
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
                        </Box>
                        {!currentUser && (
                            <>
                                <Button color="inherit" onClick={() => navigate(AppRoutes.LoginPage)}>Login</Button>
                                <Button color="inherit"
                                        onClick={() => navigate(AppRoutes.RegisterPage)}>Register</Button>
                            </>
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
            <Container sx={{my: 2}}>
                <Outlet/>
            </Container>
        </Box>
    )
}

export default Layout;