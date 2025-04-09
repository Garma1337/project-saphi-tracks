import {CustomTrack, DiscordGuildWidget} from "../lib/api/dtos.ts";
import randomSlice from "../utils/randomSlice.ts";
import ApiClient from "../lib/services/apiClient.ts";
import {useEffect, useState } from "react";

const useIndexViewModel = (apiClient: ApiClient) => {
    const [discordGuildWidget, setDiscordGuildWidget] = useState<DiscordGuildWidget | null>(null);
    const [discordGuildWidgetLoadingError, setDiscordGuildWidgetLoadingError] = useState<string | null>(null);
    const [highlightedTracks, setHighlightedTracks] = useState<CustomTrack[]>([]);

    useEffect(() => {
        apiClient.getDiscordStatus().then((status) => {
            if (status.success) {
                setDiscordGuildWidget(status.widget);
            } else {
                setDiscordGuildWidgetLoadingError(status.error);
            }
        });
    }, [setDiscordGuildWidget, setDiscordGuildWidgetLoadingError]);

    useEffect(() => {
        apiClient.findCustomTracks(null, null, null, true, null, 1, 10).then((query) => {
            const items = query.items || [];
            const randomTracks: CustomTrack[] = randomSlice(items, 3);

            setHighlightedTracks(randomTracks);
        });
    }, [setHighlightedTracks]);

    return {
        discordGuildWidget,
        discordGuildWidgetLoadingError,
        highlightedTracks,
    }
}

export default useIndexViewModel;