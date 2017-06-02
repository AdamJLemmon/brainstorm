var Web3 = require('web3');
window.web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));

$("#login").on('click', function () {
    var username = $('#user_name').val();
    var password = $('#password').val();

    // username and password cannot be blank
    if (username && password){
        console.log('login attempt: ' + username + ' ' + password)

        $.ajax({
            url: '/attempt_login',
            data: {
                'username': username,
                'password': password
            },
            dataType: 'json',
            success: function (data) {

                // alert message if not successful
                if (data['state'] != 'success'){
                    alert(data['state'])
                }
                else {
                    console.log(data['state'])
                    window.location.href = window.location.href + "dashboard/" + data['username']
                    // big hack - TODO: remove
                    window.user = data['username'];
                }

            } // success fn
        });// ajax req
    }
    else {
        alert("Username and password can not be blank")
    }
});



$("#register").on('click', function () {

    var username = $('#reg_user_name').val();
    var password = $('#reg_password').val();
    var email = $('#reg_email').val();

    console.log('Create user: ' + username + ' ' + password)

    $.ajax({
        url: '/create_user',
        data: {
            'username': username,
            'password': password,
            'email': email
        },
        dataType: 'json',
        success: function (data) {
            // if user create successful then create eth account
            if (data['state'] != 'success'){
                alert(data['state'])
            } // if statement
            else {
                $('#register-modal').modal('hide')
                console.log("Creating eth account...");
                // success so create eth account then update user accounts
                window.web3.personal.newAccount(password, function(error, result){
                    if(!error){
                        console.log(result);
                        // update user account in mongo
                        updateUserAccounts(username, result)
                        window.location.href = window.location.href + "dashboard/" + data['username']
                    } else {
                        console.log(error);
                        // TODO: remove user if cannot connect to ethereum node
                        // window.location.href = window.location.href + "remove_user/"
                    }
                });
            }
        } // success fn
    }); // ajax req
});

$("#forgotpassword").on('click', function () {
    //
    window.location.href = window.location.href + "change_password/"
});

function updateUserAccounts(username, newAccount){
    // var update = {"$push": {"accounts": newAccount}}

    $.ajax({
        url: '/update_user',
        data: {
            'username': username,
            'action': "$set",
            'attr': "account_address",
            'accountAddr': newAccount
        },
        dataType: 'json',
        success: function (data) {
            console.log(data)
        } // success fn
    }); // ajax req
}


$("#get_tokens").on('click', function () {
    var username = $('#username')[0].innerHTML;
    var balance = 0;
    var account_address = "";

    console.log('getting tokens for user: ' + username )

    $.ajax({
        url: '/get_account_address',
        data: {
            'username': username
        },
        dataType: 'json',
        success: function (data) {
            if (data['state'] != 'success'){
                alert(data['state'])
            } // if statement
            else {
                account_address = data['account_address'];
                balance = get_balance(account_address);
                update_balance(username, balance);
                $('#balance')[0].innerHTML = balance;

                window.web3.eth.defaultAccount = window.web3.eth.accounts[0];
                window.web3.personal.unlockAccount(window.web3.eth.accounts[0], "geth");

                console.log(account_address);

                if(window.web3.eth.accounts[0] != account_address){
                    var tx = window.web3.eth.sendTransaction({from:window.web3.eth.accounts[0], to: account_address, value: web3.toWei(50, "ether")});
                    console.log(tx);
                    add_transaction(tx);
                }
            }
        }
    });
});


$("#update_balance").on('click', function () {

    var username = $('#username')[0].innerHTML;
    var balance = 0;
    var account_address = "";

    console.log('getting tokens for user: ' + username )

    $.ajax({
        url: '/get_account_address',
        data: {
            'username': username
        },
        dataType: 'json',
        success: function (data) {
            if (data['state'] != 'success'){
                alert(data['state'])
            }
            else {
                account_address = data['account_address'];
                balance = get_balance(account_address);
                update_balance(username, balance);
                $('#balance')[0].innerHTML = balance;
            }
        }
    });
});

function get_balance(account) {
    var balance = window.web3.fromWei(window.web3.eth.getBalance(account))
    return balance.c[0];
}

function update_balance(username, balance) {
//    console.log('updating balance')
    $.ajax({
        url: '/update_balance',
        data: {
            'username': username,
            'balance': balance
        },
        dataType: 'json',
        success: function (data) {
            if (data['state'] != 'success'){
                alert(data['state'])
            }
            else {
                console.log("balance updated")
            }
        }
    });
}


function add_transaction(txID){
    // TODO: add style to div - add timestamp, status, value, etc
    var transaction_div = document.createElement("div");
    var txID_text = document.createElement("p");
    txID_text.innerHTML = txID;
    transaction_div.appendChild(txID_text);
    var transaction_container = document.getElementById("dashboard-transaction-container")
    transaction_container.appendChild(transaction_div);
}






