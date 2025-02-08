use crate::models::custom_track::CustomTrack;
use crate::models::permission::Permission;
use crate::models::user::User;

pub struct PermissionResolver {

}

impl PermissionResolver {
    pub fn can_edit_custom_track(custom_track: CustomTrack, permission: Permission) -> bool {
        permission.user_id == custom_track.author_id || permission.can_edit_custom_tracks
    }

    pub fn can_delete_custom_track(permission: Permission) -> bool {
        permission.can_delete_custom_tracks
    }

    pub fn can_edit_resource(permission: Permission) -> bool {
        permission.can_edit_resources
    }

    pub fn can_delete_resources(permission: Permission) -> bool {
        permission.can_delete_resources
    }

    pub fn can_edit_user(user: User, permission: Permission) -> bool {
        permission.user_id == user.id || permission.can_edit_users
    }

    pub fn can_see_unverified_custom_track(custom_track: CustomTrack, permission: Permission) -> bool {
        (permission.user_id == custom_track.author_id) || (permission.can_edit_custom_tracks && permission.can_delete_custom_tracks)
    }

    pub fn can_see_unverified_user(user: User, permission: Permission) -> bool {
        permission.user_id == user.id || permission.can_edit_users
    }

    pub fn can_upload_verified_custom_tracks(permission: Permission) -> bool {
        permission.can_edit_custom_tracks && permission.can_delete_custom_tracks
    }

}
