# Color My Quilt

The idea is to build a website that can upload a photo of a quilt, and the program will match the quilt colors with the Kona Solids quilt fabrics that are needed in the quilt.

Will need to address colors showing up differently in different lights. Would be amazing if it could also return a google search of that fabric IRL?

![Screenshot of Color My Quilt](static/assets/img/color_my_quilt_screenshot.png "Color My Quilt Demo")

## TODO

* How to store uploaded photo on client side instead of server? How do websites handle this?
* Add Kona color palette matching (i.e. show 5 related colors and let user click 1)
* Add google search to return kona fabrics in the wild?
* Return Kona Color Chart Group (i.e. Leaf is in group "G")
* Add ability to get "similar hex" colors
* Add ability to increase or decrease brightness of selected image?
* Improve button UI
* Add ability to toggle between hex and rgb
* Add Stripe API for funsies
* What if the file name of the RK fabric is not standard? Build web scraper to get url of tile using code instead of hardcoding?  
* Don't show fabric tile if none are selected (currently is defualted) 
* Show "No fabric found" if no results are returned
* Create a new page that is a list of the robert kaufman fabric pictures and rgb matches
* Consider taking multiple pixels of fabric in scraper and averaging them to avoid the 1 weird pixel

## Buggies

* "No file chosen" is shown as text even when image is still shown