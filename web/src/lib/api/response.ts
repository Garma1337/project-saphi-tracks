export type Pagination = {
    current_page: number;
    items_per_page: number;
    total_item_count: number;
    total_page_count: number;
}

export type PaginatedQuery = {
    pagination: Pagination;
    items: any[];
}
