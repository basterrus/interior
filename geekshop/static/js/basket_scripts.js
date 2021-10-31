window.onload = function () {
    $('.basket_item').on('click', 'input[type="number"]', function () {
        var t_href = event.target;

        $.ajax({
            url: "/basket/edit/" + t_href.name + "/" + t_href.value + "/",

            success: function (data) {
                $('.basket_item').html(data.result);
            },
        });

        event.preventDefault();
    });
}