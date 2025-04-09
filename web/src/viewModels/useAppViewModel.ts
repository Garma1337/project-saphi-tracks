import { useEffect, useState } from "react";
import ApiClient from "../lib/services/apiClient.ts";
import SessionManager from "../lib/services/sessionManager.ts";
import {Setting, Tag, User} from "../lib/api/dtos.ts";

const useAppViewModel = (
    apiClient: ApiClient,
    sessionManager: SessionManager,
) => {
    const [settings, setSettings] = useState<Setting[]>([]);
    const [tags, setTags] = useState<Tag[]>([]);
    const [currentUser, setCurrentUser] = useState<User | null>(null);
    const [displayOptions, setDisplayOptions] = useState(new Map());

    useEffect(() => {
        sessionManager.getSession().then((response) => {
            setCurrentUser(response.current_user);
            setDisplayOptions(new Map(Object.entries(response.display_options)));
        });
    }, [setCurrentUser, setDisplayOptions]);

    useEffect(() => {
        apiClient.findSettings(null, null, null, null, null).then(query => setSettings(query.items));
    }, [setSettings]);

    useEffect(() => {
        apiClient.findTags(null, null, null, null).then(query => setTags(query.items));
    }, [setTags]);

    return {
        settings,
        tags,
        currentUser,
        displayOptions,
    };
}

export default useAppViewModel;