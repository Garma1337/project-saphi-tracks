use crate::models::custom_track::CustomTrack;
use crate::schema::custom_tracks;
use diesel::prelude::*;

pub struct CustomTrackRepository {
    pub connection: PgConnection,
}

impl CustomTrackRepository {
    pub fn new(connection: PgConnection) -> Self {
        CustomTrackRepository { connection }
    }

    pub fn find_one(&mut self, track_id: i32) -> QueryResult<CustomTrack> {
        custom_tracks::table.find(track_id).first(&mut self.connection)
    }

    pub fn find(&mut self) -> QueryResult<Vec<CustomTrack>> {
        custom_tracks::table.load::<CustomTrack>(&mut self.connection)
    }

    pub fn create(&mut self, new_track: &CustomTrack) -> QueryResult<CustomTrack> {
        diesel::insert_into(custom_tracks::table)
            .values(new_track)
            .get_result(&mut self.connection)
    }

    pub fn update(&mut self, track_id: i32, updated_track: &CustomTrack) -> QueryResult<CustomTrack> {
        diesel::update(custom_tracks::table.find(track_id))
            .set(updated_track)
            .get_result(&mut self.connection)
    }
}
