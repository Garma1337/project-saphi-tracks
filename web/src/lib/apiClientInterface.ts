import {
    CreateCustomTrackResponse,
    LoginResponse,
    PaginatedQueryResponse,
    SessionResponse,
    VerifyCustomTrackResponse,
    VerifyResourceResponse
} from "./api/response.ts";

export default interface ApiClientInterface {
    createCustomTrack: (
        name: string,
        description: string,
        video: string,
        previewImage: File,
        levFile: File,
        levFileVersion: string,
        vrmFile: File,
        vrmFileVersion: string,
    ) => Promise<CreateCustomTrackResponse>
    findCustomTracks: (
        id: number | null,
        authorId: number | null,
        name: string | null,
        highlighted: boolean | null,
        verified: boolean | null,
        page: number | null,
        perPage: number | null,
    ) => Promise<PaginatedQueryResponse>
    findPermissions: (
        id: number | null,
        userId: number | null,
        page: number | null,
        perPage: number | null,
    ) => Promise<PaginatedQueryResponse>
    findResources: (
        id: number | null,
        page: number | null,
        perPage: number | null,
    ) => Promise<PaginatedQueryResponse>
    findSettings: (
        id: number | null,
        category: string | null,
        key: string | null,
        page: number | null,
        perPage: number | null,
    ) => Promise<PaginatedQueryResponse>
    findTags: (
        id: number | null,
        name: string | null,
        page: number | null,
        perPage: number | null,
    ) => Promise<PaginatedQueryResponse>
    findUsers: (
        id: number | null,
        name: string | null,
        verified: boolean | null,
        page: number | null,
        perPage: number | null,
    ) => Promise<PaginatedQueryResponse>
    getSession: () => Promise<SessionResponse>,
    login: (
        username: string,
        password: string
    ) => Promise<LoginResponse>,
    verifyCustomTrack: (
        id: number
    ) => Promise<VerifyCustomTrackResponse>,
    verifyResource: (
        id: number
    ) => Promise<VerifyResourceResponse>,
}
