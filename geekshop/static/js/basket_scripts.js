window.onload = function(){
    $('.basket_record').on('click', 'input[type=number]', function(){
        let t_href = event.target;

        $.ajax({
            url: '/basket/edit/' + t_href.name + '/' + t_href.value + '/',
            success: function(data){
                $('.basket_record').html(data.result);
            }
        });
        return false;
    });
};