import { useState } from "react";
import ApiClient from "../lib/services/apiClient.ts";

const useCustomTrackCreateViewModel = (
    apiClient: ApiClient,
    resetForm: () => void,
) => {
    const [customTrackCreateSuccess, setCustomTrackCreateSuccess] = useState(false);
    const [customTrackCreateError, setCustomTrackCreateError] = useState<string | null>(null);

    const createCustomTrack = (
        name: string,
        description: string,
        video: string,
        previewImage: File | null,
        levFile: File | null,
        vrmFile: File | null,
        levFileVersion: string,
        vrmFileVersion: string,
    ) => {
        setCustomTrackCreateSuccess(false);
        setCustomTrackCreateError(null);

        apiClient.createCustomTrack(
            name || '',
            description || '',
            video || '',
            previewImage || new File([], ''),
            levFile || new File([], ''),
            levFileVersion || '',
            vrmFile || new File([], ''),
            vrmFileVersion || '',
        ).then((response) => {
            if (response.success) {
                setCustomTrackCreateSuccess(true);
                resetForm();
            } else {
                setCustomTrackCreateError(response.error);
            }
        });
    }

    return {
        customTrackCreateSuccess,
        customTrackCreateError,
        createCustomTrack,
    }
}

export default useCustomTrackCreateViewModel;