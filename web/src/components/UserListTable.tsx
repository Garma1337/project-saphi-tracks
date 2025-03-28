import {
    Button,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Typography
} from "@mui/material";
import {Link, useNavigate} from "react-router-dom";
import AppRoutes from "../routes.tsx";
import formatDate from "../utils/formatDate.ts";
import ZoomInIcon from '@mui/icons-material/ZoomIn';
import {User} from "../lib/api/dtos.ts";

interface UserListTableProps {
    users: User[]
}

const UserListTable = (props: UserListTableProps) => {
    const navigate = useNavigate();

    return (
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
                    {props.users.map((row) => (
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
    )
}

export default UserListTable;