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

const uploaded_img = document.getElementById();

// When user clicks on image, get color using Pythong pyautogui library
// Update the "color-swatch" element accordingly
document.addEventListener('click', function(event) {
//    const x = event.clientX;
//    const y = event.clientY;

    post_body = {
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
            console.log("Color swatches: ", data.color_swatches)
            console.log("Color swatches 1: ", data.color_swatches['color-swatch-1'])

//            TODO: Put this into a method so it is less verbose
            const colorDisplay1 = document.getElementById('color-swatch-1');
            colorDisplay1.style.backgroundColor = data.color_swatches['color-swatch-1']
            colorDisplay1.style.borderColor = data.current_color == 1 ? "red" : "black"
            colorDisplay1.style.borderWidth = data.current_color == 1 ? "medium" : "thin"
            const colorText1 = document.getElementById('color-text-1');
            colorText1.textContent = data.color_swatches['color-swatch-1']

            const colorDisplay2 = document.getElementById('color-swatch-2');
            colorDisplay2.style.backgroundColor = data.color_swatches['color-swatch-2']
            colorDisplay2.style.borderColor = data.current_color == 2 ? "red" : "black"
            colorDisplay2.style.borderWidth = data.current_color == 2 ? "medium" : "thin"
            const colorText2 = document.getElementById('color-text-2');
            colorText2.textContent = data.color_swatches['color-swatch-2']

            const colorDisplay3 = document.getElementById('color-swatch-3');
            colorDisplay3.style.backgroundColor = data.color_swatches['color-swatch-3']
            colorDisplay3.style.borderColor = data.current_color == 3 ? "red" : "black"
            colorDisplay3.style.borderWidth = data.current_color == 3 ? "medium" : "thin"
            const colorText3 = document.getElementById('color-text-3');
            colorText3.textContent = data.color_swatches['color-swatch-3']

            const colorDisplay4 = document.getElementById('color-swatch-4');
            colorDisplay4.style.backgroundColor = data.color_swatches['color-swatch-4']
            colorDisplay4.style.borderColor = data.current_color == 4 ? "red" : "black"
            colorDisplay4.style.borderWidth = data.current_color == 4 ? "medium" : "thin"
            const colorText4 = document.getElementById('color-text-4');
            colorText4.textContent = data.color_swatches['color-swatch-4']

            const colorDisplay5 = document.getElementById('color-swatch-5');
            colorDisplay5.style.backgroundColor = data.color_swatches['color-swatch-5']
            colorDisplay5.style.borderColor = data.current_color == 5 ? "red" : "black"
            colorDisplay5.style.borderWidth = data.current_color == 5 ? "medium" : "thin"
            const colorText5 = document.getElementById('color-text-5');
            colorText5.textContent = data.color_swatches['color-swatch-5']
        }
    });
});

////check for Navigation Timing API support
//if (performance.navigation.type == performance.navigation.TYPE_RELOAD) {
//    console.info( "This page is reloaded" );
//    fetch('/refresh_page', {
//        method: 'POST',
//        headers: {
//            'Content-Type': 'application/json'
//        }
//    })
//}