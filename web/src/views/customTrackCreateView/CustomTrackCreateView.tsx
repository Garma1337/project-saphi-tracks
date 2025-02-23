import {Alert, Stack, TextField, Typography} from "@mui/material";
import {useState} from "react";
import useStore from "../../store.ts";

const CustomTrackCreateView = () => {
    const tags = useStore(state => state.tags);

    const [name, setName] = useState<string | null>(null);
    const [description, setDescription] = useState<string | null>(null);
    const [selectedTags, setSelectedTags] = useState<string[] | null>(null);

    const resetForm = () => {
        setName(null);
        setDescription(null);
        setSelectedTags(null);
    }

    return (
        <Stack spacing={2}>
            <Typography variant={"h4"}>Create Custom Track</Typography>

            <Alert severity="info">
                The maximum allowed file size is 5MB.
                Preview images must be 250x250 pixels.
            </Alert>

            <Stack component={"form"} spacing={2} width={"30ch"}>
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
                    value={description || ''}
                    onChange={(e) => setDescription(e.target.value)}
                />
            </Stack>
        </Stack>
    );
}

export default CustomTrackCreateView;