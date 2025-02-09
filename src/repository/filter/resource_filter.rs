pub struct ResourceFilter {
    pub id: Option<i32>,
    pub author_id: Option<i32>,
    pub custom_track_id: Option<i32>,
    pub search_text: Option<String>,
    pub resource_type: Option<String>,
    pub verified: Option<bool>,
}
