use crate::models::custom_track::CustomTrack;
use crate::repository::filter::custom_track_filter::CustomTrackFilter;
use crate::schema::custom_tracks;
use diesel::prelude::*;

pub struct CustomTrackRepository {
    pub connection: PgConnection,
}

impl CustomTrackRepository {
    pub fn new(connection: PgConnection) -> Self {
        CustomTrackRepository { connection }
    }

    pub fn find_one(&mut self, id: i32) -> QueryResult<CustomTrack> {
        custom_tracks::table.find(id).first(&mut self.connection)
    }

    pub fn find(&mut self, filter: CustomTrackFilter) -> QueryResult<Vec<CustomTrack>> {
        let mut query = custom_tracks::table.into_boxed();

        if let Some(author_id) = filter.author_id {
            query = query.filter(custom_tracks::author_id.eq(author_id));
        }

        if let Some(search_text) = filter.search_text {
            query = query.filter(custom_tracks::name.ilike(format!("%{}%", search_text)));
            query = query.filter(custom_tracks::description.ilike(format!("%{}%", search_text)));
        }

        if let Some(staff_pick) = filter.staff_pick {
            query = query.filter(custom_tracks::staff_pick.eq(staff_pick));
        }

        if let Some(verified) = filter.verified {
            query = query.filter(custom_tracks::verified.eq(verified));
        }

        query.load::<CustomTrack>(&mut self.connection)
    }

    pub fn create(&mut self, new_track: &CustomTrack) -> QueryResult<CustomTrack> {
        diesel::insert_into(custom_tracks::table)
            .values(new_track)
            .get_result(&mut self.connection)
    }

    pub fn update(
        &mut self,
        track_id: i32,
        updated_track: &CustomTrack,
    ) -> QueryResult<CustomTrack> {
        diesel::update(custom_tracks::table.find(track_id))
            .set(updated_track)
            .get_result(&mut self.connection)
    }
}
