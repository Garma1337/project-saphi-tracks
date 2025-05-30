export type CustomTrack = {
    id: number;
    author_id: number;
    name: string;
    description: string;
    created: string;
    highlighted: boolean;
    verified: boolean;
    video: string;
    author: User;
    resources: Resource[];
    tags: Tag[];
}

export type DiscordGuildWidgetMember = {
    id: string;
    username: string;
    status: string;
    avatar: string;
}

export type DiscordGuildWidget = {
    id: string;
    name: string;
    invite_link: string;
    member_count: number;
    members: DiscordGuildWidgetMember[];
}

export type Permission = {
    id: number;
    user_id: number;
    can_edit_custom_tracks: boolean;
    can_delete_custom_tracks: boolean;
    can_edit_resources: boolean;
    can_delete_resources: boolean;
    can_edit_users: boolean;
    user: User;
}

export type Resource = {
    id: number;
    author_id: number;
    custom_track_id: number;
    file_name: string;
    file_size: number;
    resource_type: string;
    checksum: string;
    version: string;
    created: string;
    verified: boolean;
    author: User;
    custom_track: CustomTrack;
}

export type Setting = {
    id: number;
    category: string;
    key: string;
    value: string;
}

export type Tag  ={
    id: number;
    name: string;
    custom_tracks: CustomTrack[];
}

export type User = {
    id: number;
    username: string;
    created: string;
    verified: boolean;
    custom_tracks: CustomTrack[];
    permission: Permission;
    resources: Resource[];
}
