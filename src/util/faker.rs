pub struct Faker {
    pub custom_tracks_count: i32,
    pub resources_count: i32,
    pub users_count: i32,
}

impl Faker {
    pub fn new(custom_tracks_count: i32, resources_count: i32, users_count: i32) -> Faker {
        Faker {
            custom_tracks_count,
            resources_count,
            users_count,
        }
    }

    pub fn fake_custom_tracks(&self) {
        for _ in 0..self.custom_tracks_count {

        }
    }
}
