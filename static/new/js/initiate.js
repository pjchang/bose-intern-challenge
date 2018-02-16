/* animation for header and logo 
-----------------------------------------*/

function resizeHeaderOnScroll() {
    const distanceY = window.pageYOffset || document.documentElement.scrollTop,
        shrinkOn = 200,
        headerEl = document.getElementById('js-header');

    if (distanceY > shrinkOn) {
        headerEl.classList.add("smaller");
    } else {
        headerEl.classList.remove("smaller");
    }
}
window.addEventListener('scroll', resizeHeaderOnScroll);

/* event listener
 -----------------------------------------*/
$('#shareModal').on('hidden.bs.modal', function() {
    $('#link_copy_indicator').css('opacity', '0')
})
$('#share_link').val(window.location.toString().split("?")[0]);
$("#share_link").click(function() {
    this.select();
    document.execCommand('copy');
    $('#link_copy_indicator').css('opacity', '1')
});

// input current year.
$(".tm-copyright-year").text(new Date().getFullYear());



 