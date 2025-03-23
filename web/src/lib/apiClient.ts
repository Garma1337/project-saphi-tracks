import axios, {AxiosInstance} from "axios";
import ApiClientInterface from "./apiClientInterface.ts";
import {
    CreateCustomTrackResponse,
    LoginResponse,
    PaginatedQueryResponse,
    SessionResponse,
    VerifyCustomTrackResponse,
    VerifyResourceResponse
} from "./api/response.ts";

export default class ApiClient implements ApiClientInterface {
    private client: AxiosInstance;

    public constructor(baseUrl: string, accessToken: string | null = null) {
        this.client = axios.create({
            baseURL: baseUrl,
            validateStatus: (status) => {
                return status >= 200 && status < 500;
            }
        });

        if (accessToken) {
            this.client.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
        }
    }

    public async createCustomTrack(
        name: string,
        description: string,
        video: string,
        previewImage: File,
        levFile: File,
        levFileVersion: string,
        vrmFile: File,
        vrmFileVersion: string,
    ): Promise<CreateCustomTrackResponse> {
        const formData = new FormData();
        formData.append('name', name);
        formData.append('description', description);
        formData.append('video', video);
        formData.append('preview_image', previewImage);
        formData.append('lev_file', levFile);
        formData.append('lev_file_version', levFileVersion);
        formData.append('vrm_file', vrmFile);
        formData.append('vrm_file_version', vrmFileVersion);

        const response = await this.client.post(`/customtracks`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });

        return response.data as CreateCustomTrackResponse;
    }

    public async findCustomTracks(
        id: number | null,
        authorId: number | null,
        name: string | null,
        highlighted: boolean | null,
        verified: boolean | null,
        page: number | null,
        perPage: number | null,
    ): Promise<PaginatedQueryResponse> {
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
        return response.data as PaginatedQueryResponse;
    }

    public async findPermissions(
        id: number | null,
        userId: number | null,
        page: number | null,
        perPage: number | null,
    ): Promise<PaginatedQueryResponse> {
        const params = {
            id: id,
            user_id: userId,
            page: page,
            per_page: perPage,
        }

        const response = await this.client.get(`/permissions`, {params});
        return response.data as PaginatedQueryResponse;
    }

    public async findResources(
        id: number | null,
        page: number | null,
        perPage: number | null,
    ): Promise<PaginatedQueryResponse> {
        const params = {
            id: id,
            page: page,
            per_page: perPage,
        }

        const response = await this.client.get(`/resources`, {params});
        return response.data as PaginatedQueryResponse;
    }

    public async findSettings(
        id: number | null,
        category: string | null,
        key: string | null,
        page: number | null,
        perPage: number | null,
    ): Promise<PaginatedQueryResponse> {
        const params = {
            id: id,
            category: category,
            key: key,
            page: page,
            per_page: perPage,
        }

        const response = await this.client.get(`/settings`, {params});
        return response.data as PaginatedQueryResponse;
    }

    public async findTags(
        id: number | null,
        name: string | null,
        page: number | null,
        perPage: number | null,
    ): Promise<PaginatedQueryResponse> {
        const params = {
            id: id,
            name: name,
            page: page,
            per_page: perPage,
        }

        const response = await this.client.get(`/tags`, {params});
        return response.data as PaginatedQueryResponse;
    }

    public async findUsers(
        id: number | null,
        name: string | null,
        verified: boolean | null,
        page: number | null,
        perPage: number | null,
    ): Promise<PaginatedQueryResponse> {
        const params = {
            id: id,
            username: name,
            verified: verified,
            page: page,
            per_page: perPage,
        }

        const response = await this.client.get(`/users`, {params});
        return response.data as PaginatedQueryResponse;
    }

    public async getSession(): Promise<SessionResponse> {
        const response = await this.client.get(`/session`);
        return response.data as SessionResponse;
    }

    public async login(username: string, password: string): Promise<LoginResponse> {
        const response = await this.client.post(`/login`, { username, password });
        return response.data as LoginResponse;
    }

    public async verifyCustomTrack(id: number): Promise<VerifyCustomTrackResponse> {
        const response = await this.client.post(`/customtracks/verify`, { id });
        return response.data as VerifyCustomTrackResponse;
    }

    public async verifyResource(id: number): Promise<VerifyResourceResponse> {
        const response = await this.client.post(`/resources/verify`, { id });
        return response.data as VerifyResourceResponse;
    }
}
