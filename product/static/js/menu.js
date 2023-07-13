var data = {
    "page": 1,
};
var block_request = false;
var end_pagination = false;

var sort_rate = 0;
var sort_price = 0;

var cate_activate = false;
var rate_activate = false;

const get_data = async(data)=>{
    await $.ajax({
        type: 'GET',
        url: window.location.href,
        data: data,
        success: function (data) {
            if (data.end_pagination === true) {
                end_pagination = true;
            } else {
                block_request = false;
            }
            $('.pro-flex').html(data.content);
        }
    })
}

const filter_categories = async(id, name)=>{
    data.page = 1;
    data.category = id;
    if (data.name){
        $("#input-food").val("");
        delete data.name;
    }
    if(data.rate){
        $("#rate-color").css({"background-color":"rgb(255, 255, 255)", "color":"rgb(156, 156, 156)"}); 
        delete data.rate;
    }
    if (sort_rate!=0){
        $("#sorted-rate").text("filter_list");
        sort_rate=0;
        delete data.by_rate;
    }
    if (sort_price!=0){
        $("#sorted-price").text("filter_list");
        sort_price=0;
        delete data.by_price;
    }
    $('#spinner-menu').addClass('d-flex');
    await get_data(data);
    $('#spinner-menu').removeClass('d-flex');
    $("#cate-name").text(name);
    $('#cate-filter').css({"background-color":"rgb(239, 79, 95)", "color":"rgb(255, 255, 255)"});
    cate_activate = true;
}

const filter_categories_cancel = async()=>{
    if (cate_activate){
        data.page = 1;
        delete data.category
        // if (data.name){
        //     $("#input-food").val("");
        //     delete data.name;
        // }
        $('#spinner-menu').addClass('d-flex');
        await get_data(data);
        $('#spinner-menu').removeClass('d-flex');

        $("#cate-name").text("All food");
        $('#cate-filter').css({"background-color":"rgb(255, 255, 255)", "color":"rgb(156, 156, 156)"});
        cate_activate = false;
    }
    
}

const rating_filter = async()=>{
    data.rate = 4;
    $('#spinner-menu').addClass('d-flex');
    await get_data(data);
    $('#spinner-menu').removeClass('d-flex');
    $("#rate-color").css({"background-color":"rgb(239, 79, 95)", "color":"rgb(255, 255, 255)"});
    rate_activate = true;
}
const rating_filter_cancel = async()=>{
    if (rate_activate){
        delete data.rate;
        $('#spinner-menu').addClass('d-flex');
        await get_data(data);
        $('#spinner-menu').removeClass('d-flex');
        $("#rate-color").css({"background-color":"rgb(255, 255, 255)", "color":"rgb(156, 156, 156)"}); 
    }  
}

const sorted_rating = async()=>{
    switch(sort_rate){
        case 0:
            data.by_rate = "asc";
            $('#spinner-menu').addClass('d-flex');
            await get_data(data);
            $('#spinner-menu').removeClass('d-flex');
            $("#sorted-rate").text("arrow_upward");
            sort_rate +=1;
            break;
        case 1:
            data.by_rate = "desc";
            $('#spinner-menu').addClass('d-flex');
            await get_data(data);
            $('#spinner-menu').removeClass('d-flex');
            $("#sorted-rate").text("arrow_downward");
            sort_rate+=1;
            break;
        default:
            delete data.by_rate;
            $('#spinner-menu').addClass('d-flex');
            await get_data(data);
            $('#spinner-menu').removeClass('d-flex');
            $("#sorted-rate").text("filter_list");
            sort_rate = 0;
    }
}

const sorted_price = async()=>{
    switch(sort_price){
        case 0:
            data.by_price = "asc";
            $('#spinner-menu').addClass('d-flex');
            await get_data(data);
            $('#spinner-menu').removeClass('d-flex');
            $("#sorted-price").text("arrow_upward");
            sort_price +=1;
            break;
        case 1:
            data.by_price = "desc";
            $('#spinner-menu').addClass('d-flex');
            await get_data(data);
            $('#spinner-menu').removeClass('d-flex');
            $("#sorted-price").text("arrow_downward");
            sort_price+=1;
            break;
        default:
            delete data.by_price;
            $('#spinner-menu').addClass('d-flex');
            await get_data(data);
            $('#spinner-menu').removeClass('d-flex');
            $("#sorted-price").text("filter_list");
            sort_price = 0;
    }
}

function add_favorites(id){
    // console.log(id);
    var url = document.getElementById(`add-favorite${id}`).getAttribute('url');
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    // console.log(csrftoken);
    var btn = $(`#add-favorite${id}`);
    btn.prop('disabled', true);
    btn.toggleClass('no-drop');
           
    $.ajax({
        type: 'POST',
        headers: { 
            "X-CSRFToken": csrftoken,
        },
        url: url,
        data: {"food_id":id},
        success: function (response) {
            console.log(response); 
            btn.prop('disabled', false);
            btn.toggleClass('no-drop');
            $(`#heart-favorite${id}`).toggleClass('fa-solid');
            $('#quantity-favorite').text(response['quantity']);
            // btn.toggleClass('toggle-favorite');
        },
        error: function(response){
            console.log(response.responseJson);
            if (response.status=401){
                $('#login-require').click();
            }
            btn.prop('disabled', false);
            btn.toggleClass('no-drop');
        }
    })
}
let food_add = {'quantity':1}
function addToTable(id,img,name,price, is_order){
    if (is_order){
        if (is_order == 'True'){
            food_add['food_id'] = id;
            $('#food_add_url').attr('src',img);
            $('#food_add_url').attr('alt',"img");
            $('#food_add_name').text(name);
            $('#food_add_price').text(`${price} vnđ`);
            $('#add_log').click();
        }
        else{
            $('#mess-log-order').text("In future, You haven't any orders.");
            $('#mess_log').click();
        }
    }
    else{
        $('#login-require').click();
    }
}
function subQuantity(){
    let quantity = parseInt($('#food_add_quantity').text());
    if (quantity>1){
        food_add['quantity'] = quantity - 1;
        $('#food_add_quantity').text(quantity - 1);
    }
}
function addQuantity(){
    let quantity = parseInt($('#food_add_quantity').text());
    food_add['quantity'] = quantity + 1;
    $('#food_add_quantity').text(quantity + 1);
}
function submitAdd(){
    $('#btn_confirm_add').prop('disabled', true);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    food_add['order_id'] = parseInt($('#select-ordered').val());
    $.ajax({
        type: 'POST',
        headers: { 
            "X-CSRFToken": csrftoken,
        },
        url: $('#btn_confirm_add').attr('url'),
        data: food_add,
        success: function (response) {
            $('#btn_confirm_add').prop('disabled', false);
            $('#mess-log-order').text("Add successfully!");
            $('#close-add').click();
            $('#mess_log').click();
            $('#mess_icon_fail').prop('hidden', true);
            $('#mess_icon_success').prop('hidden', false);
        },
        error: function(response){
            $('#btn_confirm_add').prop('disabled', false);
            // console.log(response.responseJSON);
            $('#mess-log-order').text(response.responseJSON['msg']);
            $('#close-add').click();
            $('#mess_log').click();
            $('#mess_icon_success').prop('hidden', true);
            $('#mess_icon_fail').prop('hidden', false);

            
        }
    })
}

$(document).ready(function() {
    var current = 0;
    let timer = null;
    $("#next").click(function(e){
        e.preventDefault();
        if (current< 6){
            current++;
            if (current==6){
                $("#next").attr("hidden",true);
            }
            $('#polite').css("transform",`translateX(${current*-190}px)`);
        }
        $("#pre").attr("hidden",false);
    });

    $("#pre").click(function(e){
        e.preventDefault();
        $("#next").attr("hidden",false);
        if (current>0){
            current--;
            if (current==0){
                $("#pre").attr("hidden",true);
            }
            $('#polite').css("transform",`translateX(${current*-190}px)`);
        }
    });
    
    function debounce(callback){
        if (timer) clearTimeout(timer);
        timer = setTimeout(()=>callback(),1000);
    }
    $("#input-food").on('input',function(e) {
        debounce(async()=>{
            // console.log($("#input-food").val());
        // if (e.which == 13) {
            data.page = 1;
            // if ($("#input-food").val()){
            data.name = $("#input-food").val();
            // }
            $('#spinner-menu').addClass('d-flex');
            await get_data(data);
            $('#spinner-menu').removeClass('d-flex');
        // }
        })
    });
    
    $("#search-food").click(async(e)=> {
        data.page = 1;
        // if ($("#input-food").val()){
        data.name = $("#input-food").val();
        // }
        $('#spinner-menu').addClass('d-flex');
        await get_data(data);
        $('#spinner-menu').removeClass('d-flex');
    });

    $("#cate-cancel").click(function(e) {filter_categories_cancel();});

    $("#sorted-rate").click(function(e) {sorted_rating();});

    $("#rate-filter").click(function(e) {rating_filter();});

    $('#rate-cancel').click(function(e) {rating_filter_cancel();});

    $("#sorted-price").click(function(e) {sorted_price();});

    


    // window.news_index = 'menu';
    // var page = 1;

    $(window).scroll(function () {
        var margin = $(document).height() - $(window).height() - 400;
        if ($(window).scrollTop() > margin && end_pagination === false && block_request === false) {
            block_request = true;
            data.page += 1;
            $.ajax({
                type: 'GET',
                url: window.location.href,
                data: data,
                success: function (data) {
                    if (data.end_pagination === true) {
                        end_pagination = true;
                    } else {
                        block_request = false;
                    }
                    $('.pro-flex').append(data.content);
                }
            })
        }
    });
});