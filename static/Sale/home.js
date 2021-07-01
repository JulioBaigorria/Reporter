const reportBtn = document.getElementById('report-btn')
const reportImg = document.getElementById('report-img')
const modalBody = document.getElementById('modal-body')
const alertBox = document.getElementById('alert-box')
const reportName = document.getElementById('id_name')
const reportRemarks = document.getElementById('id_remarks')
const reportForm = document.getElementById('report-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

const alertHandler = (type, msg) => {
    alertBox.innerHTML = `<div class="alert alert-${type}" role="alert">
    ${msg}
  </div>`
}

if (reportImg) {
    reportBtn.classList.remove('not-visible')
}

reportBtn.addEventListener('click', ()=> {
    
    reportImg.setAttribute('class', 'w-100')
    modalBody.prepend(reportImg)
    //con append se pone al final, con prepend al principio

    reportForm.addEventListener('submit', e=>{
        e.preventDefault()
        console.log('click')
        const formData = new FormData()
        formData.append('csrfmiddlewaretoken', csrf)
        formData.append('name', reportName.value)
        formData.append('remarks', reportRemarks.value)
        formData.append('image', reportImg.src)

        $.ajax({
            type: 'POST',
            url: '/reports/save/',
            data: formData,
            success: function(response){
                console.log(response)
                alertHandler('success', 'Reporte creado')
            },
            error: function(error){
                console.log(error)
                alertHandler('danger', 'Hubo algun error')
            },
            processData: false,
            contentType: false,

        })
    })
})

