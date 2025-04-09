import ApiClient from "../lib/services/apiClient.ts";
import {CustomTrack, User} from "../lib/api/dtos.ts";
import randomSlice from "../utils/randomSlice.ts";
import {useEffect, useState} from "react";

const useUserPageViewModel = (
    apiClient: ApiClient,
    searchParams: URLSearchParams,
)=> {
    const [user, setUser] = useState<User | null>(null);
    const [userCustomTracks, setUserCustomTracks] = useState<CustomTrack[]>([]);

    useEffect(() => {
        const id = Number(searchParams.get('id'));
        apiClient.findUsers(id, null, null, null, null).then(query => setUser(query.items[0]));
    }, [searchParams, setUser]);

    useEffect(() => {
        if (user) {
            apiClient.findCustomTracks(null, user.id, null, null, null, 1, 50).then((query) => {
                const randomTracks: CustomTrack[] = randomSlice(query.items, 6);
                setUserCustomTracks(randomTracks)
            });
        }
    }, [user, setUserCustomTracks]);

    return {
        user,
        userCustomTracks,
    }
}

export default useUserPageViewModel;