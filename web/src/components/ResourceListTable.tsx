import TableContainer from "@mui/material/TableContainer/TableContainer";
import Table from "@mui/material/Table/Table";
import TableHead from "@mui/material/TableHead/TableHead";
import TableRow from "@mui/material/TableRow/TableRow";
import TableCell from "@mui/material/TableCell/TableCell";
import {Resource} from "../lib/api/dtos.ts";
import Paper from "@mui/material/Paper/Paper";
import Link from "@mui/material/Link";
import ApiClient from "../lib/services/apiClient.ts";
import ServiceManager from "../lib/serviceManager.ts";
import Button from "@mui/material/Button/Button";

interface ResourceListTableProps {
    resources: Resource[];
    borderLess?: boolean;
}

const ResourceListTable = (props: ResourceListTableProps) => {
    const apiClient: ApiClient = ServiceManager.createApiClient();

    return (
        <TableContainer component={props.borderLess ? 'div' : Paper}>
            <Table sx={{minWidth: 650}} aria-label="User List">
                <TableHead>
                    <TableRow>
                        <TableCell>#</TableCell>
                        <TableCell>File Name</TableCell>
                        <TableCell>Version</TableCell>
                        <TableCell></TableCell>
                    </TableRow>
                </TableHead>
                {props.resources.map((resource) => (
                    <TableRow
                        key={resource.id}
                        sx={{'&:last-child td, &:last-child th': {border: 0}}}
                    >
                        <TableCell component="th" scope="row">
                            {resource.id}
                        </TableCell>
                        <TableCell>
                            {resource.file_name}
                        </TableCell>
                        <TableCell>
                            {resource.version}
                        </TableCell>
                        <TableCell align="right">
                            <Link
                                href={apiClient.proxyResource(resource)}
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                <Button variant="contained">
                                    Download
                                </Button>
                            </Link>
                        </TableCell>
                    </TableRow>
                ))}
            </Table>
        </TableContainer>
    )
}

export default ResourceListTable;