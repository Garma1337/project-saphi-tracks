import {PaginatedQuery} from "./api/response.ts";

export default interface ApiClientInterface {
    findCustomTracks: (
        id: number | null,
        authorId: number | null,
        name: string | null,
        highlighted: boolean | null,
        verified: boolean | null,
        page: number | null,
        perPage: number | null,
    ) => Promise<PaginatedQuery>
    findPermissions: (
        id: number | null,
        userId: number | null,
        page: number | null,
        perPage: number | null,
    ) => Promise<PaginatedQuery>
    findResources: (
        id: number | null,
        page: number | null,
        perPage: number | null,
    ) => Promise<PaginatedQuery>
    findSettings: (
        id: number | null,
        category: string | null,
        key: string | null,
        page: number | null,
        perPage: number | null,
    ) => Promise<PaginatedQuery>
    findTags: (
        id: number | null,
        name: string | null,
        page: number | null,
        perPage: number | null,
    ) => Promise<PaginatedQuery>
    findUsers: (
        id: number | null,
        name: string | null,
        verified: boolean | null,
        page: number | null,
        perPage: number | null,
    ) => Promise<PaginatedQuery>
}
