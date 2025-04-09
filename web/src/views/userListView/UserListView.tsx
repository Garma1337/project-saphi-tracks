import * as React from 'react';
import {useState} from 'react';
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
import ApiClient from "../../lib/services/apiClient.ts";
import RestoreIcon from "@mui/icons-material/Restore";
import ServiceManager from "../../lib/serviceManager.ts";
import UserListTable from "../../components/UserListTable.tsx";
import useUserListViewModel from '../../viewModels/useUserListViewModel.ts';

const UserListView = () => {
    const apiClient: ApiClient = ServiceManager.createApiClient();

    const [page, setPage] = useState<number>(1);
    const [name, setName] = useState<string | null>(null);

    const { users, pagination } = useUserListViewModel(
        apiClient,
        page,
        name,
    )

    const handlePageChange = (_event: React.ChangeEvent<unknown>, value: number) => {
        setPage(value);
    }

    const resetSearchForm = () => {
        setName(null);
    }

    return (
        <Stack spacing={2}>
            <Typography variant="h4">User List</Typography>

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
                    onClick={() => resetSearchForm()}
                    variant="contained"
                    color="secondary"
                    size="large"
                    sx={{padding: 1.75}}
                >
                    <RestoreIcon sx={{marginRight: 1}}/>
                    Reset
                </Button>
            </Box>
            {users.length > 0 && (
                <>
                    <MuiPagination
                        count={pagination?.total_page_count}
                        shape={"rounded"}
                        color={"primary"}
                        size={"large"}
                        page={page}
                        onChange={handlePageChange}
                        sx={{marginBottom: 2}}
                    />
                    <UserListTable users={users} borderLess={true} />
                    <MuiPagination
                        count={pagination?.total_page_count}
                        shape={"rounded"}
                        color={"primary"}
                        size={"large"}
                        page={page}
                        onChange={handlePageChange}
                        sx={{marginTop: 2}}
                    />
                </>
            )}
            {users.length === 0 && <Alert severity="warning" variant="filled">No users match the search.</Alert>}
        </Stack>
    );
}

export default UserListView;