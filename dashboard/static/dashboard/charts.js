function onMonthClick(month) {
    setFilter("month", month);
}

options: {
    onClick: (evt, elements) => {
        if (elements.length > 0) {
            const index = elements[0].index;
            onMonthClick(chart.data.labels[index]);
        }
    }
}
