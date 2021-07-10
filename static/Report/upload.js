
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
const alertBox = document.getElementById('alert-box')
Dropzone.autoDiscover = false

const alertHandler = (type, msg) => {
    alertBox.innerHTML = `<div class="alert alert-${type}" role="alert">
    ${msg}
  </div>`
}

const myDropzone = new Dropzone('#my-dropzone', {
    url: '/reports/upload/',
    init: function(){
        this.on('sending', function(file, xhr, formData){
            console.log('sending')
            formData.append('csrfmiddlewaretoken', csrf)
        })
        this.on('success', function(file, response){
            if(response.ex){
               alertHandler(type='danger', msg='file already exists')
            }else{
                alertHandler(type='success', msg='file uploaded') 
            }
        })
    },
    maxFiles: 3,
    maxFilesize: 3,
    acceptedFiles: '.csv'
})