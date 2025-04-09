import {useEffect, useState } from "react";
import {User} from "../lib/api/dtos.ts";
import {Pagination} from "../lib/api/response.ts";
import ApiClient from "../lib/services/apiClient.ts";

const useUserListViewModel = (
    apiClient: ApiClient,
    page: number,
    name: string | null,
) => {
    const [users, setUsers] = useState<User[]>([]);
    const [pagination, setPagination] = useState<Pagination | null>(null);

    useEffect(() => {
        apiClient.findUsers(null, name, null, page, null).then((query) => {
            setPagination(query.pagination);
            setUsers(query.items || []);
        });
    }, [name, page, setPagination, setUsers]);

    return {
        users,
        pagination,
    }
}

export default useUserListViewModel;