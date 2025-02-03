pub struct Pagination {
    pub current_page: i32,
    pub items_per_page: i32,
    pub total_items: i32,
}

impl Pagination {
    pub fn new(current_page: i32, items_per_page: i32, total_items: i32) -> Self {
        Pagination {
            current_page,
            items_per_page,
            total_items,
        }
    }

    pub fn get_current_page(&self) -> i32 {
        self.current_page
    }

    pub fn get_items_per_page(&self) -> i32 {
        self.items_per_page
    }

    pub fn get_total_items(&self) -> i32 {
        self.total_items
    }

    pub fn get_total_pages(&self) -> i32 {
        (self.total_items as f64 / self.items_per_page as f64).ceil() as i32
    }

    pub fn get_offset(&self) -> i32 {
        (self.current_page - 1) * self.items_per_page
    }

    pub fn get_next_page(&self) -> i32 {
        if self.current_page < self.get_total_pages() {
            self.current_page + 1
        } else {
            self.current_page
        }
    }

    pub fn get_previous_page(&self) -> i32 {
        if self.current_page > 1 {
            self.current_page - 1
        } else {
            self.current_page
        }
    }

    pub fn has_next_page(&self) -> bool {
        self.current_page < self.get_total_pages()
    }

    pub fn has_previous_page(&self) -> bool {
        self.current_page > 1
    }
}
