
const get_data = async(data)=>{
    await $.ajax({
        type: 'GET',
        url: window.location.href,
        data: data,
        success:  function (response) {
            // console.log(response.content);
            if (response.content !=''){
                $('#list-food-filter').html(response.content);
                $('#food-filter').addClass('show');
            }
            else{
                $('#food-filter').removeClass('show');
            }
            
        }
    })
}
let listItemsSelected = {};
function total_money(){
    let total = 0;
    for (const [key, value] of Object.entries(listItemsSelected)) {
        total  += value.quantity*value.price*1000;
    }
    total = new Intl.NumberFormat("de-DE").format(total);
    $("#total-money").text(`${total} vnđ`);
}
function addQuantity(id){
    if (listItemsSelected[id]){
        listItemsSelected[id].quantity += 1;
        $(`#quantity${id}`).text(listItemsSelected[id].quantity);
        total_money();
    }
}
function subQuantity(id){
    if (listItemsSelected[id]){
        listItemsSelected[id].quantity -= 1;
        total_money();
        if (listItemsSelected[id].quantity <= 0){
            $(`#item${id}`).remove();
            delete listItemsSelected[id];
            if (Object.keys(listItemsSelected).length === 0){
                $('#no-food-selected').prop('hidden', false);
            }
        }
        else{
            $(`#quantity${id}`).text(listItemsSelected[id].quantity);
        }
    }
}
function removeFood(id){
    $(`#item${id}`).remove();
    delete listItemsSelected[id];
    total_money();
    if (Object.keys(listItemsSelected).length === 0){
        $('#no-food-selected').prop('hidden', false);
        $('.total-money').prop('hidden', true);
    }
}
function addFood(e,product){
    product = product.replaceAll("'",'"');
    product = JSON.parse(product);
    product['quantity'] = 1;
    listItemsSelected[product.id] = product; 
    $('#no-food-selected').prop('hidden', true);
    $('.total-money').prop('hidden', false);
    if ($(`#item${product.id}`).length == 0){
        let newDiv = document.createElement('li');
        newDiv.setAttribute('id', `item${product.id}`);
        newDiv.innerHTML = `
        <div>
        <img src="${product.url_img}" alt="">
        </div>
        <div style="justify-content: flex-start;">${product.name}</div>
        <div>${product.price} vnđ</div>
        <div>
            <button type='button' onclick="subQuantity(${product.id})">-</button>
            <div id='quantity${product.id}' class="count">${product.quantity}</div>
            <button type='button' onclick="addQuantity(${product.id})">+</button>
        </div>
        <div>
            <i onclick='removeFood(${product.id})' class="fa-solid fa-trash fa-xl"></i>
        </div>
        `;
        $('.selected-food').append(newDiv);
        total_money();
    }
    // console.log(listItemsSelected);
}

let listfriends = [];
function removeFriend(id){
    $(`#selected-friend-${id}`).remove();
    var index = listfriends.indexOf(id);
    if (index !== -1) {
        listfriends.splice(index, 1);
    }
    // console.log(listfriends);
}
function addFriend(id, name){
    if (listfriends.length < (parseInt($('#select1').val()-1)) && !listfriends.includes(id)){
        listfriends.push(id);
        let newDiv = document.createElement('div');
        newDiv.setAttribute('id', `selected-friend-${id}`);
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
                <div onclick='removeFriend(${id})' style="cursor: pointer;">
                    <i class="fa-solid fa-xmark fa-lg"></i>
                </div>
            </div>
        `;
        $('#partner-selected').append(newDiv);
    }
}

$(document).ready(function() {

    $(document).on('click',function(divclose){
        if ($(divclose.target).closest('#food-filter').length ==0){
            $('#food-filter').removeClass('show');
        }
        if ($(divclose.target).closest('#partner-filter').length ==0){
            $('#partner-filter').removeClass('show');
        }
    });
    
    $('#search-food').on('click',function(){
        food_name = {'food-name':$("#input-booking").val()};
            get_data(food_name);
    });
    $("#input-booking").on('input',function(e) {
            food_name = {'food-name':$("#input-booking").val()};
            get_data(food_name);
    });
    $('#input-partner').prop('disabled',true);
    $('#search-partner').click(function(){
        let filter = $('#input-partner').val();
        $.ajax({
            type: 'GET',
            url: $('#search-partner').attr('name'),
            data: {'filter': filter},
            success:  function (response) {
                // console.log(response['id']);
                let newDiv = document.createElement('li');
                newDiv.setAttribute('id', `friend${response['id']}`);
                newDiv.innerHTML = `
                    <img src=${response['img']} alt=${response['name']}>
                    <div>
                        <span style="width: 200px;">${response['name']}</span>
                        <span>${filter}</span>
                    </div>
                    <div>
                        <i onclick="addFriend(${response['id']},'${response['name']}')" class="fa-solid fa-circle-plus fa-2xl"></i>
                    </div>
                `;
                $('#list-partner-filter').html(newDiv);
                $('#partner-filter').addClass('show');
            },
            error: function(){
                let newDiv = document.createElement('li');
                newDiv.innerHTML = `
                    <div style='width:333px;justify-content:end'>
                        <span style="width: 200px;">Not found.</span>
                    </div>
                `;
                $('#list-partner-filter').html(newDiv);
                $('#partner-filter').addClass('show');
            }
        })
    });
    let timer = null;
    function debounce(callback){
        if (timer) clearTimeout(timer);
        timer = setTimeout(()=>callback(),1000);
    }
    $('#input-partner').on('input',function(){
        debounce(()=>{
            let filter = $('#input-partner').val();
            $.ajax({
                type: 'GET',
                url: $('#search-partner').attr('name'),
                data: {'filter': filter},
                success:  function (response) {
                    // console.log(response['id']);
                    let newDiv = document.createElement('li');
                    newDiv.setAttribute('id', `friend${response['id']}`);
                    newDiv.innerHTML = `
                        <img src=${response['img']} alt=${response['name']}>
                        <div>
                            <span style="width: 200px;">${response['name']}</span>
                            <span>${filter}</span>
                        </div>
                        <div>
                            <i onclick="addFriend(${response['id']},'${response['name']}')" class="fa-solid fa-circle-plus fa-2xl"></i>
                        </div>
                    `;
                    $('#list-partner-filter').html(newDiv);
                    $('#partner-filter').addClass('show');
                },
                error: function(){
                    let newDiv = document.createElement('li');
                    newDiv.innerHTML = `
                        <div style='width:333px;justify-content:end'>
                            <span style="width: 200px;">Not found.</span>
                        </div>
                    `;
                    $('#list-partner-filter').html(newDiv);
                    $('#partner-filter').addClass('show');
                }
            })
        },)
    });
    $('#select1').on('change',function(e) {
        let value = parseInt($(this).val());
        if (value>1){
            $('#input-partner').prop('disabled',false);
        }else{
            $('#input-partner').prop('disabled',true);
        }
        if((value-1) <listfriends.length){
            let revid = listfriends.pop();
            $(`#selected-friend-${revid}`).remove();
        }
    });

    $('#form-booking').submit(function(e) {
        e.preventDefault();
        $(".on-submit").each(function() {
            $(this).prop('disabled', true);
        });
        let name = $('#name-input').val();
        let email = $('#email-input').val();
        let phone = $('#phone-input').val();
        let date = $('#date-input').val();
        let noOfPeople = $('#select1').val();
        let special_request = $('#request-input').val();
        let booking_data ={
            'name':name,
            'email':email,
            'phone': phone,
            'date':date,
            'noOfPeople':noOfPeople,
            'foods': listItemsSelected,
            'special_request': special_request,
            'partner': listfriends
        }
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
         $.ajax({
            type: 'POST',
            headers: {"X-CSRFToken": csrftoken,},
            url: window.location.href,
            data: {'booking_data':JSON.stringify( booking_data)},
            success: function (res) {
                $('#mess-log-order').text('Booking successful. Go to menu?');
                $("#mess_log").click();
                $('#mess_icon_fail').prop('hidden', true);
                $('#mess_icon_success').prop('hidden', false);
                $(".on-submit").each(function() {
                    $(this).prop('disabled', false);
                });
                $('#btn_confirm_mess').click(function(e){
                    e.preventDefault();
                    var url = document.getElementById('btn_confirm_mess').getAttribute('url');
                    window.location.href = url;
                })
            },
            error: function (error){
                let msg = error.responseJSON['msg'];
                console.log(msg);
                $(".on-submit").each(function() {
                    $(this).prop('disabled', false);
                });
                $('#mess-log-order').text(msg);
                $("#mess_log").click();
                $('#mess_icon_success').prop('hidden', true);
                $('#mess_icon_fail').prop('hidden', false);
                $('#btn_confirm_mess').click(function(e){
                    e.preventDefault();
                })
            }
        })
    });
});