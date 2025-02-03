#[cfg(test)]
mod tests {
    use crate::helpers::pagination::Pagination;

    #[test]
    pub fn test_should_get_current_page() {
        let pagination = Pagination::new(1, 10, 100);
        assert_eq!(pagination.get_current_page(), 1);
    }

    #[test]
    pub fn test_should_get_items_per_page() {
        let pagination = Pagination::new(1, 10, 100);
        assert_eq!(pagination.get_items_per_page(), 10);
    }

    #[test]
    pub fn test_should_get_total_items() {
        let pagination = Pagination::new(1, 10, 100);
        assert_eq!(pagination.get_total_items(), 100);
    }

    #[test]
    pub fn test_should_get_total_pages() {
        let pagination = Pagination::new(1, 10, 100);
        assert_eq!(pagination.get_total_pages(), 10);
    }

    #[test]
    pub fn test_should_get_total_pages_with_remainder() {
        let pagination = Pagination::new(1, 10, 105);
        assert_eq!(pagination.get_total_pages(), 11);
    }

    #[test]
    pub fn test_should_get_total_pages_when_total_items_is_less_than_items_per_page() {
        let pagination = Pagination::new(1, 10, 5);
        assert_eq!(pagination.get_total_pages(), 1);
    }

    #[test]
    pub fn test_should_get_offset() {
        let pagination = Pagination::new(1, 10, 100);
        assert_eq!(pagination.get_offset(), 0);
    }

    #[test]
    pub fn test_should_get_offset_for_page_two() {
        let pagination = Pagination::new(2, 10, 100);
        assert_eq!(pagination.get_offset(), 10);
    }

    #[test]
    pub fn test_should_get_next_page() {
        let pagination = Pagination::new(1, 10, 100);
        assert_eq!(pagination.get_next_page(), 2);
    }

    #[test]
    pub fn test_should_get_next_page_when_current_page_is_last_page() {
        let pagination = Pagination::new(10, 10, 100);
        assert_eq!(pagination.get_next_page(), 10);
    }

    #[test]
    pub fn test_should_get_previous_page() {
        let pagination = Pagination::new(2, 10, 100);
        assert_eq!(pagination.get_previous_page(), 1);
    }

    #[test]
    pub fn test_should_get_previous_page_when_current_page_is_first_page() {
        let pagination = Pagination::new(1, 10, 100);
        assert_eq!(pagination.get_previous_page(), 1);
    }

    #[test]
    pub fn test_should_return_if_pagination_has_next_page() {
        let pagination = Pagination::new(1, 10, 100);
        assert_eq!(pagination.has_next_page(), true);
    }

    #[test]
    pub fn test_should_return_if_pagination_has_next_page_when_current_page_is_last_page() {
        let pagination = Pagination::new(10, 10, 100);
        assert_eq!(pagination.has_next_page(), false);
    }

    #[test]
    pub fn test_should_return_if_pagination_has_previous_page() {
        let pagination = Pagination::new(2, 10, 100);
        assert_eq!(pagination.has_previous_page(), true);
    }

    #[test]
    pub fn test_should_return_if_pagination_has_previous_page_when_current_page_is_first_page() {
        let pagination = Pagination::new(1, 10, 100);
        assert_eq!(pagination.has_previous_page(), false);
    }
}
