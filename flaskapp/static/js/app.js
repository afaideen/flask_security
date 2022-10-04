


//use DOM method
idInputHexFile = document.getElementById('hexfile');
idConnect = document.getElementById('connect');
idErase = document.getElementById('erase');
idVerify = document.getElementById('verify');
idCheckVersion = document.getElementById('check_version');
idIpAddrBrd = document.getElementById('ip_address_brd');
idIpAddrBrd.addEventListener("blur", checkInputIpAddr);


idProgressBar = document.getElementById('progress_bar');
idProgram = document.getElementById('program');
idRunApp = document.getElementById('run_app');

idStatus = document.getElementById('status');
idStatus.innerHTML = 'Please enter valid board ip address';

var a = null;
var count_null = null;

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
    idProgram.disabled = false;
    //use jquery method
//    $('#program').prop('disabled', false);
    console.log("Enabling 'Program' button...")

}

function runApp(ip_address_brd) {
fetch('run_app/' + ip_address_brd, {
        method: "GET"
      }).then(function(response)
    {
        response.json().then(function(data)
        {
            console.log(data);
            if(data.status == 'success')
            {
                idStatus.innerHTML = "New app is running"

            }

        });

    });

}
function verify(ip_address_brd) {
    let formData = new FormData();
    formData.append("file", idInputHexFile.files[0]);
    idStatus.innerHTML = "Verifying checksum...Wait..."

    fetch('verify/' + ip_address_brd, {
        method: "POST",
        body: formData
      }).then(function(response)
    {
        response.json().then(function(data)
        {
            console.log(data);
            if(data.status == 'success')
            {
                idRunApp.disabled = false;
                idStatus.innerHTML = "Checksum verified valid. You can activate the new app."

            }
            else
            {
                idRunApp.disabled = true;
                idStatus.innerHTML = "Checksum found invalid!"
            }

        });

    });

}
function uploadFile(ip_address, ip_address_brd) {
      count_null = 0
      idProgressBar.style.width = '0%';
      idProgressBar.innerHTML = '0%';
      if(idInputHexFile.files.length == 0 )
      {
        idStatus.innerHTML = "Load your hex file.";
        return;
      }
      idProgram.disabled = true
      let formData = new FormData();
      formData.append("file", idInputHexFile.files[0]);
      fetch('/upload_file/' + ip_address_brd, {
        method: "POST",
        body: formData
      }).then(function(response){
        response.json().then(function(data){
            console.log(data);
            if( data.status == 'success')
            {
                idStatus.innerHTML = "Hex file uploaded successfully";
                idVerify.disabled = false

            }
            else
            {
                idStatus.innerHTML = "Oops, somethin wrong happened! Try again.";
                idVerify.disabled = true
            }
        });
      });
      b = setTimeout(updateProgressBar, 300, ip_address);


    //  alert('The file has been uploaded successfully.');
}

function updateProgressBar(ip_address)
{
    if(idInputHexFile.files.length == 0 )
        return;

    console.log('fetching api...read_progress_value/' + ip_address)

    fetch('read_progress_value/' + ip_address).then(function(response)
    {
        response.json().then(function(data)
        {
            console.log(data);
            v = parseInt(data.progress_value);
            if(data.progress_value != null && v <= 100)
            {
                idProgressBar.style.width = v + '%';
                idProgressBar.innerHTML = v + '%';
                if(v < 100)
                    updateProgressBar(ip_address);


            }

        });

    });
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
    idStatus.innerHTML = 'Connecting to ' + ip_val + ' ...Just wait...'

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
            else
            {
                idStatus.innerHTML = "Can't connect to the board. Try again."
            }

        });
    });
}

