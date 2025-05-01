/*!
* Start Bootstrap - Clean Blog v6.0.9 (https://startbootstrap.com/theme/clean-blog)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-clean-blog/blob/master/LICENSE)
*/

/***************** Event Listeners *******************/

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

const uploaded_img = document.getElementById('user-img');

/* When user clicks on image, get color using Pythong pyautogui library
Update the "color-swatch" element accordingly */
if (document.getElementById('user-img') != null) {

    uploaded_img.addEventListener('click', function(event) {

        post_body = {pixel_ratio: window.devicePixelRatio}

        fetch('/get_pixel_color', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(post_body)
        })
        .then(response => response.json()) // response.json --> {1: "#fffff", 2: "#85829b", 3: "#433d4e" ....}
        .then(data => {

            if (data.error) {
                console.error("Error:", data.error)
            } else {

            updateColorSwatchesHtml(data.color_swatches, data.next_color)

            }
        });
    });
}

// Add Event Listeners to all Color Swatches so that user can change selected color
const elements = document.querySelectorAll('.color-swatch');

elements.forEach(element => {

    element.addEventListener('click', function(event) {

        // Pass over selected swatch number (i.e. 1, 2, 3)
        post_body = {'selected_swatch' : element.getAttribute('data-num')}

        // Call python server to keep variables in sync
        fetch('/update_current_color', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(post_body)
        })
        .then(response => response.json()) // response.json --> {1: "#fffff", 2: "#85829b", 3: "#433d4e" ....}
        .then(data => {
            updateColorSwatchesHtml(data.color_swatches, data.next_color)
        });
    });
});

document.getElementById('get-fabric-btn').addEventListener('click', (e) => {

    post_body = {'hello' : 'world'}

    fetch('/get_fabric_match', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(post_body)
    })
    .then(response => response.json()) // response.json --> {1: "#fffff", 2: "#85829b", 3: "#433d4e" ....}
    .then(data => {

        console.log('Data: ', data)
        const fabricImg = document.getElementById("fabric-img-1");
        fabricImg.src = data.path
        const fabricText = document.getElementById("fabric-text-1");
        fabricText.textContent = data.name

    });
});

/***************** Helper Functions *******************/

/**
 * Loop through each key and set the html color swatch and text based upon return data
 * @param Map colorSwatches - Dictionary where key is the color swatch number and the value is the hex color
 * @param Int next_color - Number of the color swatch that should be "selected" (highlighted) as next
 * @returns Void No return value
 */
function updateColorSwatchesHtml(colorSwatches, next_color){

    for (const key in colorSwatches) {

        hexColor = colorSwatches[key]["hex"]
        rgbColor = colorSwatches[key]["rgb"]

        // Update the Color Swatch with the correct Hex Color
        const colorSwatchId = 'color-swatch-' + key;
        const colorSwatch = document.getElementById(colorSwatchId);
        colorSwatch.style.backgroundColor = hexColor;
        colorSwatch.style.borderColor = next_color == key ? "red" : "black"
        colorSwatch.style.borderWidth = next_color == key ? "medium" : "thin"

        // Update the Hex Color Text below the color swatch
        const colorTextId = 'color-text-' + key;
        const colorText = document.getElementById(colorTextId);
        colorText.textContent = hexColor

    }

}


//
//// When user clicks on image, get color using Pythong pyautogui library
//// Update the "color-swatch" element accordingly
//document.addEventListener('click', function(event) {
////    const x = event.clientX;
////    const y = event.clientY;
//
//    post_body = {
//        pixel_ratio: window.devicePixelRatio
//    }
//
//    fetch('/get_pixel_color', {
//        method: 'POST',
//        headers: {
//            'Content-Type': 'application/json'
//        },
//        body: JSON.stringify(post_body)
//    })
//    .then(response => response.json())
//    .then(data => {
//        if (data.error) {
//            console.error("Error:", data.error)
//        } else {
//            console.log("Color swatches: ", data.color_swatches)
//            console.log("Color swatches 1: ", data.color_swatches['color-swatch-1'])
//
////            TODO: Put this into a method so it is less verbose
//            const colorDisplay1 = document.getElementById('color-swatch-1');
//            colorDisplay1.style.backgroundColor = data.color_swatches['color-swatch-1']
//            colorDisplay1.style.borderColor = data.current_color == 1 ? "red" : "black"
//            colorDisplay1.style.borderWidth = data.current_color == 1 ? "medium" : "thin"
//            const colorText1 = document.getElementById('color-text-1');
//            colorText1.textContent = data.color_swatches['color-swatch-1']
//
//            const colorDisplay2 = document.getElementById('color-swatch-2');
//            colorDisplay2.style.backgroundColor = data.color_swatches['color-swatch-2']
//            colorDisplay2.style.borderColor = data.current_color == 2 ? "red" : "black"
//            colorDisplay2.style.borderWidth = data.current_color == 2 ? "medium" : "thin"
//            const colorText2 = document.getElementById('color-text-2');
//            colorText2.textContent = data.color_swatches['color-swatch-2']
//
//            const colorDisplay3 = document.getElementById('color-swatch-3');
//            colorDisplay3.style.backgroundColor = data.color_swatches['color-swatch-3']
//            colorDisplay3.style.borderColor = data.current_color == 3 ? "red" : "black"
//            colorDisplay3.style.borderWidth = data.current_color == 3 ? "medium" : "thin"
//            const colorText3 = document.getElementById('color-text-3');
//            colorText3.textContent = data.color_swatches['color-swatch-3']
//
//            const colorDisplay4 = document.getElementById('color-swatch-4');
//            colorDisplay4.style.backgroundColor = data.color_swatches['color-swatch-4']
//            colorDisplay4.style.borderColor = data.current_color == 4 ? "red" : "black"
//            colorDisplay4.style.borderWidth = data.current_color == 4 ? "medium" : "thin"
//            const colorText4 = document.getElementById('color-text-4');
//            colorText4.textContent = data.color_swatches['color-swatch-4']
//
//            const colorDisplay5 = document.getElementById('color-swatch-5');
//            colorDisplay5.style.backgroundColor = data.color_swatches['color-swatch-5']
//            colorDisplay5.style.borderColor = data.current_color == 5 ? "red" : "black"
//            colorDisplay5.style.borderWidth = data.current_color == 5 ? "medium" : "thin"
//            const colorText5 = document.getElementById('color-text-5');
//            colorText5.textContent = data.color_swatches['color-swatch-5']
//        }
//    });
//});

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

