import {CustomTrack, DiscordGuildWidget, Resource, User} from "./dtos.ts";

export type Pagination = {
    current_page: number;
    items_per_page: number;
    total_item_count: number;
    total_page_count: number;
}

export type PaginatedQueryResponse = {
    pagination: Pagination;
    items: any[];
}

export type CreateCustomTrackResponse = {
    success: boolean;
    error: string | null;
    custom_track: CustomTrack | null;
}

export type DeleteCustomTrackResponse = {
    success: boolean;
    error: string | null;
    message: string | null;
}

export type DiscordStatusResponse = {
    success: boolean;
    error: string | null;
    widget: DiscordGuildWidget | null;
}

export type DownloadResourceResponse = {
    file: Blob;
    content_disposition: string;
}

export type SessionResponse = {
    current_user: User;
    display_options: Map<string, boolean>;
}

export type LoginResponse = {
    success: boolean;
    access_token: string | null;
    current_user: User | null;
    error: string | null;
}

export type UpdateCustomTrackResponse = {
    success: boolean;
    error: string | null;
    custom_track: CustomTrack | null;
}

export type VerifyCustomTrackResponse = {
    success: boolean;
    error: string | null;
    custom_track: CustomTrack | null;
}

export type VerifyResourceResponse = {
    success: boolean;
    error: string | null;
    resource: Resource | null;
}
