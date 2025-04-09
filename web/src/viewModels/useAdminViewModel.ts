import ApiClient from "../lib/services/apiClient.ts";
import {CustomTrack, User} from "../lib/api/dtos.ts";
import {Pagination} from "../lib/api/response.ts";
import {useEffect, useState} from "react";

const useAdminViewModel = (
    apiClient: ApiClient,
    customTrackPage: number,
    userPage: number
) => {
    const [unverifiedCustomTracks, setUnverifiedCustomTracks] = useState<CustomTrack[]>([]);
    const [unverifiedUsers, setUnverifiedUsers] = useState<User[]>([]);

    const [customTrackPagination, setCustomTrackPagination] = useState<Pagination | null>(null);
    const [userPagination, setUserPagination] = useState<Pagination | null>(null);

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

    return {
        unverifiedCustomTracks,
        unverifiedUsers,
        customTrackPagination,
        userPagination,
    }
}

export default useAdminViewModel;