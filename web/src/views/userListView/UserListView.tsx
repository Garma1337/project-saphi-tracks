import * as React from 'react';
import {useEffect, useState} from 'react';
import {
    Alert,
    Box,
    Button,
    FormControl,
    Pagination as MuiPagination,
    Paper,
    Stack,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    TextField,
    Typography
} from "@mui/material";
import {Link, useNavigate} from "react-router-dom";
import AppRoutes from "../../routes.tsx";
import ApiClient from "../../lib/apiClient.ts";
import formatDate from "../../utils/formatDate.ts";
import RestoreIcon from "@mui/icons-material/Restore";
import ZoomInIcon from '@mui/icons-material/ZoomIn';
import {Pagination} from "../../lib/api/response.ts";
import ServiceManager from "../../lib/serviceManager.ts";

const UserListView = () => {
    const apiClient: ApiClient = ServiceManager.createApiClient();

    const navigate = useNavigate();
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
                    color="warning"
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
                    <TableContainer component={Paper}>
                        <Table sx={{minWidth: 650}} aria-label="PBs">
                            <TableHead>
                                <TableRow>
                                    <TableCell>#</TableCell>
                                    <TableCell align="center">Name</TableCell>
                                    <TableCell align="center">Registered since</TableCell>
                                    <TableCell align="center">Custom Tracks</TableCell>
                                    <TableCell align="center"></TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {users.map((row) => (
                                    <TableRow
                                        key={row.id}
                                        sx={{'&:last-child td, &:last-child th': {border: 0}}}
                                    >
                                        <TableCell component="th" scope="row">
                                            {row.id}
                                        </TableCell>
                                        <TableCell align="center">
                                            <Typography
                                                onClick={() => navigate(`${AppRoutes.UserDetailPage}?id=${row.id}`)}>
                                                <Link to="#">{row.username}</Link>
                                            </Typography>
                                        </TableCell>
                                        <TableCell align="center">{formatDate(row.created)}</TableCell>
                                        <TableCell align="center">{row.custom_tracks.length}</TableCell>
                                        <TableCell align="center">
                                            <Link to={`${AppRoutes.UserDetailPage}?id=${row.id}`}>
                                                <Button variant="outlined" color="primary">
                                                    <ZoomInIcon sx={{marginRight: 1}}/>
                                                    Profile
                                                </Button>
                                            </Link>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
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
            {users.length === 0 && <Alert severity={"warning"}>No users match the search.</Alert>}
        </Stack>
    );
}

export default UserListView;