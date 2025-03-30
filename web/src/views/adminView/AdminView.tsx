import {useEffect, useState} from "react";
import ApiClient from "../../lib/services/apiClient.ts";
import ServiceManager from "../../lib/serviceManager.ts";
import {CustomTrack, User} from "../../lib/api/dtos.ts";
import {Pagination} from "../../lib/api/response.ts";
import Tabs from "@mui/material/Tabs/Tabs";
import Tab from "@mui/material/Tab/Tab";
import TabContent from "../../components/TabContent.tsx";
import CustomTrackListGrid from "../../components/CustomTrackListGrid.tsx";
import {Alert, Box, Pagination as MuiPagination, Stack} from "@mui/material";
import UserListTable from "../../components/UserListTable.tsx";
import useStore from "../../store.ts";
import { useNavigate } from "react-router-dom";
import AppRoutes from "../../routes.tsx";

const AdminView = () => {
    const apiClient: ApiClient = ServiceManager.createApiClient();

    const navigate = useNavigate();
    const displayOptions = useStore(state => state.displayOptions);

    const [unverifiedCustomTracks, setUnverifiedCustomTracks] = useState<CustomTrack[]>([]);
    const [unverifiedUsers, setUnverifiedUsers] = useState<User[]>([]);

    const [customTrackPagination, setCustomTrackPagination] = useState<Pagination | null>(null);
    const [customTrackPage, setCustomTrackPage] = useState<number>(1);

    const [userPagination, setUserPagination] = useState<Pagination | null>(null);
    const [userPage, setUserPage] = useState<number>(1);

    const [tabIndex, setTabIndex] = useState(0);

    useEffect(() => {
        apiClient.findCustomTracks(null, null, null, null, false, customTrackPage, null).then((query) => {
            setUnverifiedCustomTracks(query.items || []);
            setCustomTrackPagination(query.pagination);
        });
    }, [setUnverifiedCustomTracks, setCustomTrackPagination, customTrackPage]);

    useEffect(() => {
        apiClient.findUsers(null, null, false, userPage, null).then((query) => {
            setUnverifiedUsers(query.items || []);
            setUserPagination(query.pagination);
        });
    }, [setUnverifiedUsers, setUserPagination, userPage]);

    const handleChange = (_event: React.SyntheticEvent, newValue: number) => {
        setTabIndex(newValue);
    };

    const handleCustomTrackPageChange = (_event: React.ChangeEvent<unknown>, value: number) => {
        setCustomTrackPage(value);
    }

    const handleUserPageChange = (_event: React.ChangeEvent<unknown>, value: number) => {
        setUserPage(value);
    }

    const createTabProperties = (index: number) => {
        return {
            'id': `simple-tab-${index}`,
            'aria-controls': `simple-tabpanel-${index}`,
        };
    }

    useEffect(() => {
        if (!displayOptions.get('show_admin_button')) {
            navigate(AppRoutes.IndexPage);
        }
    }, [displayOptions, navigate]);

    return (
        <Box sx={{width: '100%'}}>
            <Box sx={{borderBottom: 1, borderColor: 'divider'}}>
                <Tabs value={tabIndex} onChange={handleChange} aria-label="basic tabs example">
                    <Tab label="Unverified Tracks" {...createTabProperties(0)} />
                    <Tab label="Unverified Users" {...createTabProperties(1)} />
                </Tabs>
            </Box>
            <TabContent value={tabIndex} index={0}>
                <Stack spacing={2}>
                    {unverifiedCustomTracks.length === 0 && (
                        <Alert severity="success" variant="filled">There are currently no unverified custom tracks.</Alert>
                    )}

                    {unverifiedCustomTracks.length > 0 && (
                        <>
                            <MuiPagination
                                count={customTrackPagination?.total_page_count}
                                shape={"rounded"}
                                color={"primary"}
                                size={"large"}
                                page={customTrackPage}
                                onChange={handleCustomTrackPageChange}
                            />
                            <CustomTrackListGrid customTracks={unverifiedCustomTracks}/>
                            <MuiPagination
                                count={customTrackPagination?.total_page_count}
                                shape={"rounded"}
                                color={"primary"}
                                size={"large"}
                                page={customTrackPage}
                                onChange={handleCustomTrackPageChange}
                            />
                        </>
                    )}
                </Stack>
            </TabContent>
            <TabContent value={tabIndex} index={1}>
                <Stack spacing={2}>
                    {unverifiedUsers.length === 0 && (
                        <Alert severity="success" variant="filled">There are currently no unverified users.</Alert>
                    )}

                    {unverifiedUsers.length > 0 && (
                        <>
                            <MuiPagination
                                count={userPagination?.total_page_count}
                                shape={"rounded"}
                                color={"primary"}
                                size={"large"}
                                page={userPage}
                                onChange={handleUserPageChange}
                            />
                            <UserListTable users={unverifiedUsers}/>
                            <MuiPagination
                                count={userPagination?.total_page_count}
                                shape={"rounded"}
                                color={"primary"}
                                size={"large"}
                                page={userPage}
                                onChange={handleUserPageChange}
                            />
                        </>
                    )}
                </Stack>
            </TabContent>
        </Box>
    );
}

export default AdminView;