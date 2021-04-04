$(document).ready(function () {
    // -----------------------------------------------
    // Sortable table columns
    // -----------------------------------------------
    const urlParams = new URLSearchParams(window.location.search);

    $('[sortable]').each(function () {
        let element = $(this)

        let sortName = element.attr('sortable');

        let sortTypeParamKey = 'sort-' + sortName;
        let sortType = urlParams.get(sortTypeParamKey);

        let iconName = 'fa-sort';
        if (sortType === 'asc')
            iconName = 'fa-sort-down'
        else if (sortType === 'desc')
            iconName = 'fa-sort-up'

        element.append(`<span class="icon has-text-warning"><i class="fas ` + iconName + `"></i></span> `)

        element.click(function () {

            // sort order is none -> asc -> desc -> none
            if (sortType === 'asc')
                urlParams.set(sortTypeParamKey, 'desc');
            else if (sortType === 'desc')
                urlParams.delete(sortTypeParamKey);
            else
                urlParams.set(sortTypeParamKey, 'asc');

            window.location.search = urlParams.toString();
        })
    });
});