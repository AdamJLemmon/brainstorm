// function in order to dynamically attach listener
function logout(){
    $.ajax({
            url: '/logout',
            data: {},
            dataType: 'json',
            success: function (data) {
                // hide the logout button
                $('#logout_btn').hide()

                // Clear the container fields
                $('#user_name').val("")
                $('#password').val("")

                // hide the user in nav bar
                // fade in the user name in nav bar
                $('#user_icon').hide()

                // show the login button once successful
                $('#login_nav').show()

                // manual reset to home page
                window.location = '/'
            } // success fn
        });// ajax req
}


// update UI after a successful login
function loginSuccessful(username){
        // hide the login button once successful
        $('#login_nav').hide()

        // hide the login container
        $('#login_container').fadeOut();

        // add a logout button
        $('#logout_btn').show()

        // fade in the user name in nav bar
        $('#username').text("User: " + username)
        $('#user_icon').fadeIn()

        // manual push to dashboard
        window.location = '/dashboard'
}

// LOGIN Listener
$("#login_attempt").on('click', function () {
    var username = $('#user_name').val();
    var password = $('#password').val();

    // username and password cannot be blank
    if (username && password){
        console.log('login attempt: ' + username + ' ' + password)

        $.ajax({
            url: '/login_attempt',
            data: {
                'username': username,
                'password': password
            },
            dataType: 'json',
            success: function (data) {

                // alert message if not successful
                if (data['response']){
                    alert(data['response'])
                }
                else {
                    console.log('Successful login')
                    loginSuccessful(username)
                }

            } // success fn
        });// ajax req
    }
    else {
        alert("Username and password can not be blank")
    }
});


// Logout
$('#logout_btn').on('click', function(){
    logout()
})


// on click on button when user looking to create new account
$("#create_account").on('click', function () {

    // $('#loading-icon').show()

    var username = $('#reg_user_name').val();
    var password = $('#reg_password').val();
    var email = $('#reg_email').val();

    console.log('Create user: ' + username + ' ' + password)
    
    // ensure no blank fields
    if (username && password && email) {

        $.ajax({
            url: '/create_account',
            data: {
                'username': username,
                'password': password,
                'email': email
            },
            dataType: 'json',
            success: function (data) {

                // if there was a response then something went wrong, show error
                if (data['response']){
                    alert(data['response'])
                }

                // success! hide window
                else {
                    console.log('User created successfully')
                    $('#register-modal').modal('hide')
                    // $('#loading-icon').hide()
                    loginSuccessful(username)
                }
            } // success fn
        }); // ajax req
    } // outer if for form fields being present

    else
        alert('Fields cannot be left blank')
        
});