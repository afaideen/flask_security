


//use DOM method
idConnect = document.getElementById('connect');
idErase = document.getElementById('erase');
idVerify = document.getElementById('verify');
idCheckVersion = document.getElementById('check_version');
idIpAddrBrd = document.getElementById('ip_address_brd');
idIpAddrBrd.addEventListener("blur", checkInputIpAddr);


idProgressBar = document.getElementById('progress_bar');
idProgram = document.getElementById('program');

idStatus = document.getElementById('status');
idStatus.innerHTML = 'Please enter valid board ip address';

var a = null;

function enableConnectButton()
{
    if( a != null )
        clearTimeout(a);
     a = setTimeout(function(){
            if(ValidateIPaddress(idIpAddrBrd))
            {
                idConnect.disabled = false;
                clearTimeout(a);
                idStatus.innerHTML = 'Ip address format is valid. Press button to connect with the board.';

//                idIpAddrBrd.addEventListener("keyup", checkInputIpAddr);
            }
            else
            {
                idConnect.disabled = true;
                idStatus.innerHTML = 'Please enter valid board ip address';
            }

     }, 5000);



}

function checkInputIpAddr()
{
    if(ValidateIPaddress(idIpAddrBrd))
    {
        idConnect.disabled = false;
        clearTimeout(a);
        idStatus.innerHTML = 'Ip address format is valid. Press button to connect with the board.';
    }

}

//var hasFocus = $('#idIpAddrBrd').is(':focus');
//if(!hasFocus){
//    if(ValidateIPaddress(idIpAddrBrd))
//    {
//        idConnect.disabled = false;
//        clearTimeout(a);
//        idStatus.innerHTML = 'Ip address format is valid. Press button to connect with the board.';
//    }
//}

function ValidateIPaddress(inputText)
 {
     var ipformat = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
     if(inputText.value.match(ipformat))
     {
         return true;
     }
     else
     {
//         alert("You have entered an invalid IP address!");
         return false;
     }
 }

function enableProgramButton()
{
//    classProgressBar= document.getElementsByClassName('progress-bar');
    idProgram.disabled = false;

    //use jquery method
//    $('#program').prop('disabled', false);
    console.log("Enabling 'Program' button...")

}

function checkVersion(ip_val)
{
    console.log('Checking version...');
    fetch('/check_version/' + ip_val).then(function(response){
        response.json().then(function(data){
            console.log(data);
            //eg access data.status, data.version
            if( data.status == 'success')
            {
                idProgram.disabled = false
                idStatus.innerHTML = "Bootloader firmware version is " + data.version
            }

        });
    });
}

function eraseFlash(ip_val)
{
    console.log('Erasing flash...');
    fetch('/erase_flash/' + ip_val).then(function(response){
        response.json().then(function(data){
            console.log(data);
            //eg access data.status, data.version
            if( data.status == 'success')
            {
                enableProgramButton();
                idStatus.innerHTML = "Flash erased. Upload your hex file and press Program button"
            }
            else
            {
                idProgram.disabled = true;
                idStatus.innerHTML = "Flash erase failed"
            }

        });
    });

}

function connect_brd(ip_val)
{
    console.log('Connecting to ' + ip_val + ' ...Just wait...');
    fetch('/connect/' + ip_val).then(function(response){
        response.json().then(function(data){
            console.log(data);
            //eg access data.status, data.version
            if( data.status == 'success')
            {
                idErase.disabled = false;
                idCheckVersion.disabled = false;
                idStatus.innerHTML = "Board successfully connected. Bootloader firmware version is " + data.version
            }

        });
    });
}

function updateProgressBar(ip_address)
{


    console.log('fetching api...read_progress_value/' + ip_address)

    fetch('read_progress_value/' + ip_address).then(function(response)
    {
        response.json().then(function(data)
        {
            console.log(data);
            if(data.progress_value != null)
            {
                idProgressBar.style.width = data.progress_value;
                idProgressBar.innerHTML = data.progress_value;

            }
            updateProgressBar(ip_address);

        });

    });
}