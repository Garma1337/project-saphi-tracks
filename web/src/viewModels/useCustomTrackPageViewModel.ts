import { useEffect, useState } from "react";
import {CustomTrack, Resource} from "../lib/api/dtos.ts";
import randomSlice from "../utils/randomSlice.ts";
import ApiClient from "../lib/services/apiClient.ts";
import AppRoutes from "../routes.tsx";
import { useNavigate } from "react-router-dom";

const useCustomTrackPageViewModel = (
    apiClient: ApiClient,
    searchParams: URLSearchParams,
) => {
    const navigate = useNavigate();

    const [customTrack, setCustomTrack] = useState<CustomTrack | null>(null);
    const [resources, setResources] = useState<Resource[]>([]);
    const [userCustomTracks, setUserCustomTracks] = useState<CustomTrack[]>([]);

    const [verifyError, setVerifyError] = useState<string | null>(null);
    const [verifySuccess, setVerifySuccess] = useState(false);

    const [deleteError, setDeleteError] = useState<string | null>(null);

    useEffect(() => {
        const id = Number(searchParams.get('id'));
        apiClient.findCustomTracks(id, null, null, null, null, null, null).then((query) => {
            setCustomTrack(query.items[0]);
        });
    }, [searchParams, setCustomTrack]);

    useEffect(() => {
        if (customTrack) {
            setResources(customTrack.resources.filter((resource) => resource.resource_type !== 'preview'));
        }
    }, [customTrack, setResources]);

    useEffect(() => {
        if (customTrack) {
            apiClient.findCustomTracks(null, customTrack.author.id, null, null, null, 1, 50).then((query) => {
                const randomTracks: CustomTrack[] = randomSlice(query.items, 6);
                setUserCustomTracks(randomTracks)
            });
        }
    }, [customTrack, setUserCustomTracks]);

    const verifyCustomTrack = async (customTrack: CustomTrack) => {
        setVerifyError(null);
        setVerifySuccess(false);

        const response = await apiClient.verifyCustomTrack(customTrack.id);
        if (response.success) {
            setCustomTrack({...customTrack, verified: true});
            setVerifySuccess(true);
        } else {
            setVerifyError(response.error);
        }
    }

    const deleteCustomTrack = async (customTrack: CustomTrack) => {
        setDeleteError(null);

        const response = await apiClient.deleteCustomTrack(customTrack.id);
        if (response.success) {
            navigate(AppRoutes.IndexPage);
        } else {
            setDeleteError(response.error);
        }
    }

    return {
        customTrack,
        resources,
        userCustomTracks,
        verifyCustomTrack,
        verifyError,
        verifySuccess,
        deleteCustomTrack,
        deleteError,
    }
}

export default useCustomTrackPageViewModel;