import {useEffect, useState} from "react";
import ApiClient from "../lib/services/apiClient.ts";
import {CustomTrack} from "../lib/api/dtos.ts";
import {Pagination} from "../lib/api/response.ts";

const useCustomTrackListViewModel = (
    apiClient: ApiClient,
    page: number,
    name: string | null,
) => {
    const [customTracks, setCustomTracks] = useState<CustomTrack[]>([]);
    const [pagination, setPagination] = useState<Pagination | null>(null);

    useEffect(() => {
        apiClient.findCustomTracks(null, null, name, null, null, page, 20).then((query) => {
            setPagination(query.pagination);
            setCustomTracks(query.items || []);
        });
    }, [name, page, setPagination, setCustomTracks]);

    return {
        customTracks,
        pagination,
    }
}

export default useCustomTrackListViewModel;