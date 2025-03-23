import {Alert, Button, Stack, TextField, Typography} from "@mui/material";
import {useEffect, useState} from "react";
import ApiClient from "../../lib/apiClient.ts";
import ServiceManager from "../../lib/serviceManager.ts";
import {useNavigate} from "react-router-dom";
import AppRoutes from "../../routes.tsx";
import useStore from "../../store.ts";

const LoginView = () => {
    const apiClient: ApiClient = ServiceManager.createApiClient();

    const navigate = useNavigate();

    const currentUser = useStore(state => state.currentUser);
    const setCurrentUser = useStore(state => state.setCurrentUser);

    const [loginError, setLoginError] = useState<string | null>(null);
    const [username, setUsername] = useState<string | null>(null);
    const [password, setPassword] = useState<string | null>(null);

    const loginPlayer = (username: string, password: string) => {
        setLoginError(null);

        apiClient.login(username, password).then((response) => {
            if (response.success) {
                localStorage.setItem('jwt', String(response.access_token));
                setCurrentUser(response.current_user);
                resetForm();
                navigate(AppRoutes.IndexPage);
            } else {
                setLoginError(response.error);
            }
        });
    }

    const resetForm = () => {
        setUsername(null);
        setPassword(null);
    }

    useEffect(() => {
        if (currentUser) {
            navigate(AppRoutes.IndexPage);
        }
    }, [currentUser]);

    return (
        <Stack spacing={2}>
            <Typography variant="h4">Login</Typography>

            <Alert severity="warning">
                Registration is only possible on records.project-saphi.com. Please create an account there, before
                attempting to log in here.
            </Alert>

            {loginError && <Alert severity="error">Failed to login: {loginError}</Alert>}

            <Stack component="form" spacing={2} width={"30ch"}>
                <TextField
                    label="Username"
                    variant="outlined"
                    value={username || ''}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <TextField
                    label="Password"
                    variant="outlined"
                    type="password"
                    value={password || ''}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <Button
                    variant="contained"
                    color="primary"
                    type="submit"
                    onClick={() => loginPlayer(String(username), String(password))}
                >
                    Login
                </Button>
            </Stack>
        </Stack>
    );
}

export default LoginView;
