/*!
* Start Bootstrap - Clean Blog v6.0.9 (https://startbootstrap.com/theme/clean-blog)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-clean-blog/blob/master/LICENSE)
*/
window.addEventListener('DOMContentLoaded', () => {
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');
    const headerHeight = mainNav.clientHeight;
    window.addEventListener('scroll', function() {
        const currentTop = document.body.getBoundingClientRect().top * -1;
        if ( currentTop < scrollPos) {
            // Scrolling Up
            if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-visible');
            } else {
                console.log(123);
                mainNav.classList.remove('is-visible', 'is-fixed');
            }
        } else {
            // Scrolling Down
            mainNav.classList.remove(['is-visible']);
            if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-fixed');
            }
        }
        scrollPos = currentTop;
    });
})

// When user clicks on image, get color
document.addEventListener('click', function(event) {
    const x = event.clientX;
    const y = event.clientY;

    var windowWidth = window.innerWidth;
    var windowHeight = window.innerHeight;
    var windowOuterHeight = window.outerHeight;
    var windowDiff = window.outerHeight - window.innerHeight
    console.log("x: " + x + " y: " + y)
    console.log("innerHeight: " + window.innerHeight + " outerHeight: " + window.outerHeight+ " windowDiff: " + windowDiff)
//    console.log("window.devicePixelRatio: " + window.devicePixelRatio)
    post_body = {
        x: x,
        y: y,
        browser_bar_height: windowDiff,
        pixel_ratio: window.devicePixelRatio
    }

    fetch('/get_pixel_color', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(post_body)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error("Error:", data.error)
        } else {

            const colorDisplay = document.getElementById('color-swatch');
            colorDisplay.style.backgroundColor = data.new_hex_color

            const colorDisplay2 = document.getElementById('color-swatch2');
            colorDisplay2.style.backgroundColor = data.mouse_hex_color
        }
    });
});