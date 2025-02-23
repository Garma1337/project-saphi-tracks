import axios, {AxiosInstance} from "axios";
import ApiClientInterface from "./apiClientInterface.ts";
import {PaginatedQuery} from "./api/response.ts";

export default class ApiClient implements ApiClientInterface {
    private client: AxiosInstance;

    public constructor(baseUrl: string) {
        this.client = axios.create({
            baseURL: baseUrl,
            headers: {
                'Content-Type': 'application/json',
            },
        });
    }

    public async findCustomTracks(
        id: number | null,
        authorId: number | null,
        name: string | null,
        highlighted: boolean | null,
        verified: boolean | null,
        page: number | null,
        perPage: number | null,
    ): Promise<PaginatedQuery> {
        const params = {
            id: id,
            author_id: authorId,
            name: name,
            highlighted: highlighted,
            verified: verified,
            page: page,
            per_page: perPage,
        }

        const response = await this.client.get(`/customtracks`, {params});
        return response.data as PaginatedQuery;
    }

    public async findPermissions(
        id: number | null,
        userId: number | null,
        page: number | null,
        perPage: number | null,
    ): Promise<PaginatedQuery> {
        const params = {
            id: id,
            user_id: userId,
            page: page,
            per_page: perPage,
        }

        const response = await this.client.get(`/permissions`, {params});
        return response.data as PaginatedQuery;
    }

    public async findResources(
        id: number | null,
        page: number | null,
        perPage: number | null,
    ): Promise<PaginatedQuery> {
        const params = {
            id: id,
            page: page,
            per_page: perPage,
        }

        const response = await this.client.get(`/resources`, {params});
        return response.data as PaginatedQuery;
    }

    public async findSettings(
        id: number | null,
        category: string | null,
        key: string | null,
        page: number | null,
        perPage: number | null,
    ): Promise<PaginatedQuery> {
        const params = {
            id: id,
            category: category,
            key: key,
            page: page,
            per_page: perPage,
        }

        const response = await this.client.get(`/settings`, {params});
        return response.data as PaginatedQuery;
    }

    public async findTags(
        id: number | null,
        name: string | null,
        page: number | null,
        perPage: number | null,
    ): Promise<PaginatedQuery> {
        const params = {
            id: id,
            name: name,
            page: page,
            per_page: perPage,
        }

        const response = await this.client.get(`/tags`, {params});
        return response.data as PaginatedQuery;
    }

    public async findUsers(
        id: number | null,
        name: string | null,
        verified: boolean | null,
        page: number | null,
        perPage: number | null,
    ): Promise<PaginatedQuery> {
        const params = {
            id: id,
            username: name,
            verified: verified,
            page: page,
            per_page: perPage,
        }

        const response = await this.client.get(`/users`, {params});
        return response.data as PaginatedQuery;
    }
}
