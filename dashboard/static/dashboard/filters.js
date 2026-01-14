const filters = {
    start_date: null,
    end_date: null,
};

function setFilter(key, value) {
    filters[key] = value;
    refreshDashboard();
}
