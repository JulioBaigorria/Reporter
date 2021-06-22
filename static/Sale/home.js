console.log("Hola mundo")

const reportBtn = document.getElementById('report-btn')
const reportImg = document.getElementById('report-img')
console.log(reportBtn)
console.log(reportImg)

if (reportImg) {
    reportBtn.classList.remove('not-visible')
}
