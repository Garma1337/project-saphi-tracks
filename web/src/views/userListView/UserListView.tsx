import * as React from 'react';
import {useEffect, useState} from 'react';
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
import {Pagination} from "../../lib/api/response.ts";
import ServiceManager from "../../lib/serviceManager.ts";
import UserListTable from "../../components/UserListTable.tsx";

const UserListView = () => {
    const apiClient: ApiClient = ServiceManager.createApiClient();

    const [pagination, setPagination] = useState<Pagination | null>(null);
    const [page, setPage] = useState<number>(1);
    const [users, setUsers] = useState<any[]>([]);

    const [name, setName] = useState<string | null>(null);

    useEffect(() => {
        apiClient.findUsers(null, name, null, page, null).then((query) => {
            setPagination(query.pagination);
            setUsers(query.items || []);
        });
    }, [name, page, setPagination, setUsers]);

    const handlePageChange = (_event: React.ChangeEvent<unknown>, value: number) => {
        setPage(value);
    }

    const resetForm = () => {
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
                    onClick={() => resetForm()}
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