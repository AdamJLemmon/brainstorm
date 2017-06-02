$("#reg_device").on('click', function () {
    var device_id = $('#device_id').val();

    // username and password cannot be blank
    if (device_id){
        console.log('Registering Device: ' + device_id)

        $.ajax({
            url: '/register_new_device',
            type: 'GET',
            data: {
                'device_id': device_id,
            },
            dataType: 'json',
            success: function (data) {
                console.log(data)
            } // success fn
        });// ajax req
    }
    else {
        alert("Please enter a device to register")
    }
});


$("#device_discovery").on('click', function () {

        $.ajax({
            url: '/discover_usb_devices',
            data: {},
            dataType: 'json',
            success: function (data) {
                $.each(data, function(index, value){
                    $('#device_container').append('<li class="device">' + value + '</li>')    
                })
            } // success fn
        });// ajax req     
});


$("#start_acquiring").on('click', function () {

        $.ajax({
            url: '/push_data',
            data: {},
            dataType: 'json',
            success: function (data) {
                console.log(data)
            } // success fn
        });// ajax req     
});



