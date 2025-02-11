use crate::services::permission_resolver::PermissionResolver;

pub struct PermissionResolverFactory {}

impl PermissionResolverFactory {
    pub fn get_permission_resolver() -> PermissionResolver {
        PermissionResolver {}
    }
}
