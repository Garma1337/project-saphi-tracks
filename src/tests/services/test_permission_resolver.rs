#[cfg(test)]

pub mod tests {
    use std::time::SystemTime;
    use crate::models::custom_track::CustomTrack;
    use crate::models::permission::Permission;
    use crate::services::permission_resolver::PermissionResolver;

    fn create_custom_track(id: i32, author_id: i32) -> CustomTrack {
        CustomTrack {
            id,
            author_id,
            name: "Yoshi's Circuit".to_string(),
            description: "The best custom track in the game".to_string(),
            date_created: SystemTime::now(),
            staff_pick: false,
            active: true,
        }
    }

    #[test]
    fn test_can_edit_own_custom_track() {
        let custom_track = create_custom_track(1, 1);

        let permission = Permission {
            id: 1,
            user_id: 1,
            can_edit_custom_tracks: true,
            can_delete_custom_tracks: false,
            can_edit_resources: false,
            can_delete_resources: false,
            can_edit_users: false,
            can_delete_users: false,
        };

        assert_eq!(PermissionResolver::can_edit_custom_track(custom_track, permission), true);
    }

    #[test]
    fn test_can_edit_other_user_custom_track() {
        let custom_track = create_custom_track(1, 2);

        let permission = Permission {
            id: 1,
            user_id: 1,
            can_edit_custom_tracks: true,
            can_delete_custom_tracks: false,
            can_edit_resources: false,
            can_delete_resources: false,
            can_edit_users: false,
            can_delete_users: false,
        };

        assert_eq!(PermissionResolver::can_edit_custom_track(custom_track, permission), true);
    }

    #[test]
    fn test_can_not_edit_other_user_custom_track() {
        let custom_track = create_custom_track(1, 2);

        let permission = Permission {
            id: 1,
            user_id: 1,
            can_edit_custom_tracks: false,
            can_delete_custom_tracks: false,
            can_edit_resources: false,
            can_delete_resources: false,
            can_edit_users: false,
            can_delete_users: false,
        };

        assert_eq!(PermissionResolver::can_edit_custom_track(custom_track, permission), false);
    }

    #[test]
    fn test_can_not_delete_own_custom_track() {
        let permission = Permission {
            id: 1,
            user_id: 1,
            can_edit_custom_tracks: false,
            can_delete_custom_tracks: false,
            can_edit_resources: false,
            can_delete_resources: false,
            can_edit_users: false,
            can_delete_users: false,
        };

        assert_eq!(PermissionResolver::can_delete_custom_track(permission), false);
    }

    #[test]
    fn test_can_delete_other_user_custom_track() {
        let permission = Permission {
            id: 1,
            user_id: 1,
            can_edit_custom_tracks: false,
            can_delete_custom_tracks: true,
            can_edit_resources: false,
            can_delete_resources: false,
            can_edit_users: false,
            can_delete_users: false,
        };

        assert_eq!(PermissionResolver::can_delete_custom_track(permission), true);
    }
}
