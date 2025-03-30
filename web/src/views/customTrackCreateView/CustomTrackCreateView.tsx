import {Alert, Button, Stack, TextField, Typography} from "@mui/material";
import {useState, useEffect, ChangeEvent} from "react";
import ServiceManager from "../../lib/serviceManager.ts";
import ApiClient from "../../lib/services/apiClient.ts";
import useStore from "../../store.ts";
import { useNavigate } from "react-router-dom";
import AppRoutes from "../../routes.tsx";

const CustomTrackCreateView = () => {
    const apiClient: ApiClient = ServiceManager.createApiClient();

    const navigate = useNavigate();
    const currentUser = useStore(state => state.currentUser);
    const displayOptions = useStore(state => state.displayOptions);

    const [name, setName] = useState<string | null>(null);
    const [description, setDescription] = useState<string | null>(null);
    const [video, setVideo] = useState<string | null>(null);
    const [previewImage, setPreviewImage] = useState<File | null>(null);
    const [levFile, setLevFile] = useState<File | null>(null);
    const [vrmFile, setVrmFile] = useState<File | null>(null);
    const [levFileVersion, setLevFileVersion] = useState<string | null>(null);
    const [vrmFileVersion, setVrmFileVersion] = useState<string | null>(null);

    const [success, setSuccess] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const createCustomTrack = () => {
        setSuccess(false);
        setError(null);

        apiClient.createCustomTrack(
            name || '',
            description || '',
            video || '',
            previewImage || new File([], ''),
            levFile || new File([], ''),
            levFileVersion || '',
            vrmFile || new File([], ''),
            vrmFileVersion || '',
        ).then((response) => {
            if (response.success) {
                setSuccess(true);
                resetForm();
            } else {
                setError(response.error);
            }
        });
    }

    const resetForm = () => {
        setName(null);
        setDescription(null);
        setVideo(null);
        setPreviewImage(null);
        setLevFile(null);
        setVrmFile(null);
        setLevFileVersion(null);
        setVrmFileVersion(null);
    }

    useEffect(() => {
        if (!displayOptions.get('show_create_custom_track_button')) {
            navigate(AppRoutes.IndexPage);
        }
    }, [currentUser, navigate]);

    return (
        <Stack spacing={2}>
            <Typography variant={"h4"}>Create Custom Track</Typography>

            {success && (
                <Alert severity="success">
                    Your custom track was created successfully! It will be available to the public after being verified by moderators.
                </Alert>
            )}

            {error && (
                <Alert severity="error">
                    Failed to create custom track: {error}
                </Alert>
            )}

            <Alert severity="info">
                The maximum allowed file size is 5MB.
                Preview images should be 340x250 pixels.
            </Alert>

            <Stack component={"form"} spacing={2} width={"60ch"}>
                <TextField
                    required
                    label="Name"
                    variant="outlined"
                    name="name"
                    value={name || ''}
                    onChange={(e) => setName(e.target.value)}
                />
                <TextField
                    required
                    label="Description"
                    variant="outlined"
                    name="description"
                    multiline
                    value={description || ''}
                    onChange={(e) => setDescription(e.target.value)}
                />
                <TextField
                    required
                    label="Video Link"
                    variant="outlined"
                    name="video"
                    value={video || ''}
                    onChange={(e) => setVideo(e.target.value)}
                />
                <TextField
                    required
                    type="file"
                    variant="outlined"
                    name="previewImage"
                    onChange={(e: ChangeEvent<HTMLInputElement>) => setPreviewImage(e.target.files?.[0] || null)}
                />
                <Stack spacing={2} direction={"row"}>
                    <TextField
                        required
                        type="file"
                        variant="outlined"
                        name="levFile"
                        onChange={(e: ChangeEvent<HTMLInputElement>) => setLevFile(e.target.files?.[0] || null)}
                    />
                    <TextField
                        required
                        label=".lev File Version"
                        variant="outlined"
                        name="levFileVersion"
                        onChange={(e) => setLevFileVersion(e.target.value)}
                    />
                </Stack>
                <Stack spacing={2} direction={"row"}>
                    <TextField
                        required
                        type="file"
                        variant="outlined"
                        name="vrmFile"
                        onChange={(e: ChangeEvent<HTMLInputElement>) => setVrmFile(e.currentTarget.files?.[0] || null)}
                    />
                    <TextField
                        required
                        label=".vrm File Version"
                        variant="outlined"
                        name="vrmFileVersion"
                        onChange={(e) => setVrmFileVersion(e.target.value)}
                    />
                </Stack>
                <Button
                    onClick={() => createCustomTrack()}
                    variant="contained"
                    color="primary"
                >
                    Submit
                </Button>
            </Stack>
        </Stack>
    );
}

export default CustomTrackCreateView;