

function enableProgramButton()
{
    //use DOM method
    idProgram = document.getElementById('program');
    idProgressBar = document.getElementById('progress_bar');
//    classProgressBar= document.getElementsByClassName('progress-bar');
    idProgram.disabled = false
//    idProgressBar.style.width = '30%'
//    idProgressBar.innerHTML='30%'
    //use jquery method
//    $('#program').prop('disabled', false);
    console.log("myFunction running...Enabling 'Program' button...")
}