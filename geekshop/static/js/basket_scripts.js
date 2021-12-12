window.onload = function(){
    $('.basket_item').on('click', 'input[type="number"]', function(){
        let t_href = event.target;
        console.log(t_href)
        $.ajax({
            url: '/basket/edit/' + t_href.name + '/' + t_href.value + '/',

            success: function(data){
                $('.basket_item').html(data.result);
            },
        });
        return false;
    });
};