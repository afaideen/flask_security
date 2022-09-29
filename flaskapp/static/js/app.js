

function enableProgramButton()
{
    //use DOM method
    idProgram = document.getElementById('program');

//    classProgressBar= document.getElementsByClassName('progress-bar');
    idProgram.disabled = false

    //use jquery method
//    $('#program').prop('disabled', false);
    console.log("myFunction running...Enabling 'Program' button...")
}

function updateProgressBar(ip_address)
{
    idProgressBar = document.getElementById('progress_bar');
    console.log('fetching api...read_progress_value/' + ip_address)
//    fetch('verify/'+ p + '/' + v).then(function(response)
    fetch('read_progress_value/' + ip_address).then(function(response)
    {
        response.json().then(function(data)
        {
            console.log(data);
            idProgressBar.style.width = data.progress_value;
            idProgressBar.innerHTML= data.progress_value;
//            if(data.progress_value != '100%')
//            {
            updateProgressBar(ip_address);
//               setTimeout(updateProgressBar(), 1000);
//            }
//            else
//               console.log('100% stop!...');
        });

    });
}