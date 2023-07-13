const get_data = async(id)=>{
    food_name = {'food-name':$(`#input-booking-${id}`).val()};
    await $.ajax({
        type: 'GET',
        url: $(`#search-food-${id}`).attr('url'),
        data: food_name,
        success:  function (response) {
            // console.log(response.content);
            if (response.content !=''){
                $(`#list-food-filter-${id}`).html(response.content);
                $(`#food-filter-${id}`).addClass('show');
            }
            else{
                $(`#food-filter-${id}`).removeClass('show');
            }

        }
    })
}
let listItemsSelected = {};
let listfriends = {};
function total_money(id){
    let total = 0;
        for (const [key, value] of Object.entries(listItemsSelected[id])) {
        total  += value.quantity*value.price*1000;
    }
    total = new Intl.NumberFormat("de-DE").format(total);
    $(`#total-money-${id}`).text(`${total} vnđ`);
}
function addQuantity(id_form,id){
    if (listItemsSelected[id_form][id]){
        listItemsSelected[id_form][id].quantity += 1;
        $(`#quantity-${id_form}-${id}`).text(listItemsSelected[id_form][id].quantity);
        total_money(id_form);
    }
}
function subQuantity(id_form,id){
    if (listItemsSelected[id_form][id]){
        listItemsSelected[id_form][id].quantity -= 1;
        total_money(id_form);
        if (listItemsSelected[id_form][id].quantity <= 0){
            $(`#item-${id_form}-${id}`).remove();
            delete listItemsSelected[id_form][id];
            if (Object.keys(listItemsSelected[id_form]).length === 0){
                $(`#no-food-${id_form}-selected`).prop('hidden', false);
                $(`money-${id_form}`).prop('hidden', true);
            }
        }
        else{
            $(`#quantity-${id_form}-${id}`).text(listItemsSelected[id_form][id].quantity);
        }
    }
}
function removeFood(id_form,id){
    $(`#item-${id_form}-${id}`).remove();
    delete listItemsSelected[id_form][id];
    total_money(id_form);
    if (Object.keys(listItemsSelected[id_form]).length === 0){
        $(`#no-food-${id_form}-selected`).prop('hidden', false);
        $(`money-${id_form}`).prop('hidden', true);
    }
}
function addFood(e,product){
    let id_form = parseInt((e.target.parentNode.parentNode.parentNode.id).replace('list-food-filter-',''));
    // console.log(id_form);

    product = product.replaceAll("'",'"');
    product = JSON.parse(product);
    product['quantity'] = 1;
    pro ={
        'id':product.id,
        'quantity':product.quantity,
        'price':product.price
    }
    listItemsSelected[id_form][product.id] = pro;
    $(`#no-food-${id_form}-selected`).prop('hidden', true);
    $(`.money-${id_form}`).prop('hidden', false);
    if ($(`#item-${id_form}-${product.id}`).length == 0){
        let newDiv = document.createElement('li');
        newDiv.setAttribute('id', `item-${id_form}-${product.id}`);
        newDiv.innerHTML = `
        <div>
        <img src="${product.url_img}" alt="">
        </div>
        <div style="justify-content: flex-start;">${product.name}</div>
        <div id='price-${id_form}-${product.id}'>${product.price} vnđ</div>
        <div>
            <button type='button' onclick="subQuantity(${id_form},${product.id})">-</button>
            <div id='quantity-${id_form}-${product.id}' class="count">${product.quantity}</div>
            <button type='button' onclick="addQuantity(${id_form},${product.id})">+</button>
        </div>
        <div>
            <i onclick='removeFood(${id_form},${product.id})' class="fa-solid fa-trash fa-xl"></i>
        </div>
        `;
        $(`#selected-food-${id_form}`).append(newDiv);
        total_money(id_form);
    }
    // console.log(listItemsSelected);
}
function handleSubmit(e, id, customer_id){
    e.preventDefault();
    let date = $(`#date-input-${id}`).val();
    let noOfPeople = $(`#select-${id}`).val();
    let special_request = $(`#request-input-${id}`).val();
    let booking_data ={
        'customer_id':customer_id,
        'id':id,
        'date':date,
        'noOfPeople':noOfPeople,
        'foods': listItemsSelected[id],
        'special_request': special_request,
        'partner': listfriends[id]
    }
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    // console.log(booking_data);
     $.ajax({
        type: 'POST',
        headers: {"X-CSRFToken": csrftoken,},
        url: window.location.href,
        data: {'booking_data':JSON.stringify( booking_data)},
        success: function (res) {
            $('#mess-log-order').text('Update successful');
            $("#mess_log").click();
            $('#mess_icon_fail').prop('hidden', true);
            $('#mess_icon_success').prop('hidden', false);
            $('#btn_confirm_mess').click(function(e){
                e.preventDefault();
                location.reload();
            });
            $('#btn-close-mess').click(function(e){
                e.preventDefault();
                location.reload();
            });
        },
        error: function (error){
            let msg = error.responseJSON['msg'];
            // console.log(msg);
            $('#mess-log-order').text(msg);
            $('#btn_confirm_mess').prop('hidden', true);
            $('#btn_confirm_mess2').prop('hidden', false);
            $("#mess_log").click();
            $('#mess_icon_success').prop('hidden', true);
            $('#mess_icon_fail').prop('hidden', false);
        }
    })
}
function cancel_order(e, id){
    e.preventDefault();
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
    type: 'POST',
    headers: {"X-CSRFToken": csrftoken,},
    url: $(`#cancel-booking-${id}`).attr('value'),
    data: {'booking_id':id},
    success: function (res) {
        $('#mess-log-order').text('Cancel booking successful');
        $('#btn_confirm_mess').prop('hidden', true);
        $('#btn_confirm_mess2').prop('hidden', false);
        $("#mess_log").click();
        $('#mess_icon_fail').prop('hidden', true);
        $('#mess_icon_success').prop('hidden', false);
        $('#btn_confirm_mess2').click(function(e){
            e.preventDefault();
            location.reload();
        });
    },
    error: function (error){
        let msg = error.responseJSON['msg'];
        console.log(msg);
        $('#mess-log-order').text(msg);
        $('#btn_confirm_mess').prop('hidden', true);
        $('#btn_confirm_mess2').prop('hidden', false);
        $("#mess_log").click();
        $('#mess_icon_success').prop('hidden', true);
        $('#mess_icon_fail').prop('hidden', false);
    }
})
}

function removeFriend(form_id,user_id){
    $(`#select-friend-${form_id}-${user_id}`).remove();
    var index = listfriends[form_id].indexOf(user_id);
    if (index !== -1) {
        listfriends[form_id].splice(index, 1);
    }
}
function addFriend(form_id,user_id, name){
    if (!(form_id in listfriends)) {
        listfriends[form_id] = [];
    }
    if (listfriends[form_id].length < (parseInt($(`#select-${form_id}`).val()-1)) && !listfriends[form_id].includes(user_id)){
        listfriends[form_id].push(user_id);
        let newDiv = document.createElement('div');
        newDiv.setAttribute('id', `selected-friend-${form_id}-${user_id}`);
        newDiv.innerHTML = `
        <div style="    display: flex;
            width: fit-content;
            margin-right: 1rem;
            border: rgba(0,0,0,0.125) 1px solid;
            padding: 0.5rem;
            border-radius: 1.5rem;
        ">
                <span style="margin-right: 0.5rem;">
                    ${name}
                </span>
                <div onclick='removeFriend(${form_id},${user_id})' style="cursor: pointer;">
                    <i class="fa-solid fa-xmark fa-lg"></i>
                </div>
            </div>
        `;
        $(`#partner-selected-${form_id}`).append(newDiv);
    }
}
const getPartner = (id) =>{
    let filter = $(`#input-partner-${id}`).val();
    $.ajax({
        type: 'GET',
        url: $(`#search-partner-${id}`).attr('name'),
        data: {'filter': filter},
        success:  function (response) {
            let newDiv = document.createElement('li');
            // newDiv.setAttribute('id', `friend${response['id']}`);
            newDiv.innerHTML = `
                <img src=${response['img']} alt=${response['name']}>
                <div>
                    <span style="width: 200px;">${response['name']}</span>
                    <span>${filter}</span>
                </div>
                <div>
                    <i onclick="addFriend(${id},${response['id']},'${response['name']}')" class="fa-solid fa-circle-plus fa-2xl"></i>
                </div>
            `;
            $(`#list-partner-filter-${id}`).html(newDiv);
            $(`#partner-filter-${id}`).addClass('show');
        },
        error: function(){
            let newDiv = document.createElement('li');
            newDiv.innerHTML = `
                <div style='width:333px;justify-content:end'>
                    <span style="width: 200px;">Not found.</span>
                </div>
            `;
            $(`#list-partner-filter-${id}`).html(newDiv);
            $(`#partner-filter-${id}`).addClass('show');
        }
    })
}
let timer = null;
function debounce(callback){
    if (timer) clearTimeout(timer);
    timer = setTimeout(()=>callback(),1000);
}
function searchPartner(id){
    debounce(()=>{getPartner(id)});
}
function changeFriend(id){
    let value = parseInt($(`#select-${id}`).val());
    if (value>1){
        $(`#input-partner-${id}`).prop('disabled',false);
    }else{
        $(`#input-partner-${id}`).prop('disabled',true);
    }
    // console.log(listfriends[id].length);
    if((value-1) <listfriends[id].length){
        let revid = listfriends[id].pop();
        $(`#select-friend-${id}-${revid}`).remove();
    }
}
function confirmInvite(invite_id, is_accept, url){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type:'POST',
        url:url,
        headers: {"X-CSRFToken": csrftoken,},
        data:{
            'invite_id':invite_id,
            'is_accept':is_accept
        },
        success: function(response){
            $('#mess-log-order').text(response['msg']);
            $("#mess_log").click();
            $('#mess_icon_fail').prop('hidden', true);
            $('#mess_icon_success').prop('hidden', false);
            $('#btn_confirm_mess').click(function(e){
                e.preventDefault();
                location.reload();
            });
            $('#btn-close-mess').click(function(e){
                e.preventDefault();
                location.reload();
            });
        },
        error: function(error){
            let msg = error.responseJSON['msg'];
            // console.log(msg);
            $('#mess-log-order').text(msg);
            $('#btn_confirm_mess').prop('hidden', true);
            $('#btn_confirm_mess2').prop('hidden', false);
            $("#mess_log").click();
            $('#mess_icon_success').prop('hidden', true);
            $('#mess_icon_fail').prop('hidden', false);
        }
    })
}

$(document).ready(function(){
    $(document).on('click',function(divclose){
        if ($(divclose.target).closest('.food-filter').length ==0){
            $('.food-filter').removeClass('show');
        }
    });
    function setdata(){
        if ($("#list-form-ordered").has('form').length){
            let list_form = $('#list-form-ordered').children().toArray();
            // console.log(list_form);
            if (list_form.length){
                // console.log(list_form.length);
                for (let i = 0; i < list_form.length; i++){
                    let id_form = list_form[i].id;
                    // console.log(list_form[i]);
                    let list_food = {};
                    if ($(`#${id_form} #selected-food-${id_form}`).has('li').length){
                        let list_old = $(`#${id_form} #selected-food-${id_form}`).children().toArray();
                        // console.log(list_old);
                        for (let i = 0; i < list_old.length; i++){
                                let product={};
                                let id_list = list_old[i].id;
                                product['id'] = parseInt(id_list.replace(`item-${id_form}-`, ''));
                                product['quantity'] = parseInt($(`#${id_list} #quantity-${id_form}-${product['id']}`).text());
                                product['price'] = parseFloat($(`#${id_list} #price-${id_form}-${product['id']}`).text());
                                list_food[product['id']]=product;
                        }
                        listItemsSelected[id_form] = list_food;
                    }
                    else{
                        listItemsSelected[id_form] = {};
                    }
                    let list_friend = [];
                    if ($(`#${id_form} #partner-selected-${id_form}`).has('div').length){
                        let lst_fr_old = $(`#${id_form} #partner-selected-${id_form}`).children().toArray();
                        // console.log(lst_fr_old);
                        for (let i = 0; i < lst_fr_old.length; i++){
                                let id_friend = lst_fr_old[i].id;
                                let fr_id = parseInt(id_friend.replace(`select-friend-${id_form}-`, ''));
                                list_friend.push(fr_id);
                        }
                        listfriends[id_form] = list_friend;
                    }
                    else{
                        listfriends[id_form] = [];
                    }
                    // $(`#date-${id_form}`).datetimepicker({
                    //     'default': $(`#date-input-${id_form}`).val()
                    // })

                }
            }
            // console.log(listfriends);
        }

    }
    setdata();

});