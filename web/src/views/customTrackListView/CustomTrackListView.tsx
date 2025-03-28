import * as React from 'react';
import {useEffect, useState} from 'react';
import {CustomTrack} from "../../lib/api/dtos.ts";
import ApiClient from "../../lib/services/apiClient.ts";
import {
    Alert,
    Box,
    Button,
    FormControl,
    Pagination as MuiPagination,
    Stack,
    TextField,
    Typography
} from "@mui/material";
import {useNavigate} from "react-router-dom";
import AppRoutes from "../../routes.tsx";
import RestoreIcon from '@mui/icons-material/Restore';
import AddIcon from '@mui/icons-material/Add';
import {Pagination} from "../../lib/api/response.ts";
import CustomTrackListGrid from "../../components/CustomTrackListGrid.tsx";
import ServiceManager from "../../lib/serviceManager.ts";
import useStore from "../../store.ts";

const CustomTrackListView = () => {
    const apiClient: ApiClient = ServiceManager.createApiClient();

    const navigate = useNavigate();
    const displayOptions = useStore(state => state.displayOptions);

    const [customTracks, setCustomTracks] = useState<CustomTrack[]>([]);
    const [pagination, setPagination] = useState<Pagination | null>(null);
    const [page, setPage] = useState<number>(1);

    const [name, setName] = useState<string | null>(null);

    useEffect(() => {
        apiClient.findCustomTracks(null, null, name, null, null, page, 20).then((query) => {
            setPagination(query.pagination);
            setCustomTracks(query.items || []);
        });
    }, [name, page, setPagination, setCustomTracks]);

    const handlePageChange = (_event: React.ChangeEvent<unknown>, value: number) => {
        setPage(value);
    }

    const resetForm = () => {
        setPage(1);
        setName(null);
    }

    return (
        <Stack spacing={2}>
            <Typography variant="h4">Custom Track List</Typography>

            <Box>
                <FormControl sx={{minWidth: 180, marginRight: 2}}>
                    <TextField
                        label="Search ..."
                        variant="outlined"
                        name="name"
                        value={name || ''}
                        onChange={(e) => setName(e.target.value)}
                    ></TextField>
                </FormControl>

                <Button
                    onClick={() => resetForm()}
                    variant="contained"
                    color="warning"
                    size="large"
                    sx={{padding: 1.75}}
                >
                    <RestoreIcon sx={{ marginRight: 1 }}/>
                    Reset
                </Button>

                {displayOptions?.get('show_create_custom_track_button') && (
                    <Button
                        onClick={() => navigate(AppRoutes.CustomTrackCreatePage)}
                        variant="contained"
                        color="primary"
                        size="large"
                        sx={{padding: 1.75, marginLeft: 2}}
                    >
                        <AddIcon sx={{ marginRight: 1 }}/>
                        Create Custom Track
                    </Button>
                )}
            </Box>
            {customTracks.length > 0 && (
                <>
                    <MuiPagination
                        count={pagination?.total_page_count}
                        shape={"rounded"}
                        color={"primary"}
                        size={"large"}
                        page={page}
                        onChange={handlePageChange}
                    />
                    <CustomTrackListGrid customTracks={customTracks}/>
                    <MuiPagination
                        count={pagination?.total_page_count}
                        shape={"rounded"}
                        color={"primary"}
                        size={"large"}
                        page={page}
                        onChange={handlePageChange}
                    />
                </>
            )}
            {customTracks.length === 0 && <Alert severity={"warning"}>No custom tracks match the search.</Alert>}
        </Stack>
    );
}

export default CustomTrackListView;
