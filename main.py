# --------------- TODOS --------------------#

# TODO scripts.js create method to set color swatch css/html
# TODO if user clicks on a color swatch, update the "current color"
# TODO Fix bug when user refreshes the page, the colors reset to white but the global variable is still set
# TODO Add Kona color palette matching (i.e. show 5 related colors and let user click 1)
# TODO Add google search to return kona fabrics in the wild?
# TODO Return Kona Color Chart Group (i.e. Leaf is in group "G")
# TODO Add ability to get "similar hex" colors
# TODO Add ability to increase or decrease brightness of selected image?
# --------------- Imports --------------------#

from pprint import pprint
from flask import Flask, jsonify, render_template, request, send_file, redirect, url_for
from flask_bootstrap import Bootstrap5
from pyscreeze import pixel
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO
import pyautogui
import os
import pyscreeze

# ------------------- Constants and Initial Config -----------------#

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Bootstrap5(app)

current_file = None
hex_color = "#fcba03"
color_to_update = 1 # Keeps track of which swatch box is outlined in red
color_swatches = {}

# ------------------- Helper Methods -----------------#

def get_hex(rgb_color):
    return '#{:02x}{:02x}{:02x}'.format(rgb_color[0], rgb_color[1], rgb_color[2])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def set_color_data(color):
    print(f"Set color data for: {color}")
    global color_swatches
    global color_to_update

    # Dynamically create key to set hex color
    key = f"color-swatch-{color_to_update}"
    color_swatches[key] = color

    # If the color number is less than 5, increase by 1 so the next value in the set of 5 can be updated
    if color_to_update < 5:
        color_to_update += 1
    # If the color number is 5, then restart from the beginning
    else:
        color_to_update = 1

    # Pass updated color swatches and the current color
    return {'color_swatches': color_swatches, 'current_color': color_to_update}

def reset_color_swatch():
    global color_swatches
    global color_to_update

    color_to_update = 1
    color_swatches = color_swatches = {
        "color-swatch-1": "#fffff",
        "color-swatch-2": "#fffff",
        "color-swatch-3": "#fffff",
        "color-swatch-4": "#fffff",
        "color-swatch-5": "#fffff",
    }

# ------------------- URL Methods -----------------#

@app.route("/")
def home():
    reset_color_swatch()
    print(f"Color swatches in home method: {color_swatches}")
    return render_template("index.html", filename=current_file, hex_color=hex_color)


@app.route('/upload', methods=['POST'])
def upload_file():
    print("Running the Upload Method")

    global current_file

    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file and allowed_file(file.filename):
        current_file = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], current_file))
        print(f"Filename: {current_file}")

        # return render_template("index.html", filename=current_file, hex_color=hex_color)
        print("Redirct to home")
        return redirect(url_for("home"))

    return 'Invalid file type'

@app.route('/get_pixel_color', methods=['POST', 'GET'])
def get_pixel_color():
    """On user mouse click, return current pixel color

    JS Event Listener in static/js/scripts.js will pass current screen pixel ratio to method.
    This method will use pyautogui to get current mouse click coordinates, adjust using the ratio,
    and then find the current rgb color before converting into hex and returning to JS method.

    TODO: Pyautogui currently does not support multiple monitors. Eventually need to solve for this.
    One idea is to have user click button to "calibrate" screen so we can find how to adjust automatically (i.e. add 1700 to x coordnate)

    TODO: Only allow user to click on image to get colors (user can currently click anywhere)
    """

    try:
        print(f"Get pixel colors: {color_swatches}")

        data = request.get_json()
        pixel_ratio = data['pixel_ratio']

        # Get coordinates from pyautogui position() method since this will include the chrome url bar
        # Multiply coordinates by pixel ratio (as needed)
        new_x = pyautogui.position()[0] * pixel_ratio
        new_y = pyautogui.position()[1] * pixel_ratio
        print(f"Coordinates to pass to Pyautogui x: {new_x}, y: {new_y}")

        # Pixel() method is expecting chrome url bar to be included
        # Previously was trying to pass window.screen coordinates but these didn't include chrome url bar so we werent' getting the correct color
        current_rgb = pyautogui.pixel(new_x, new_y)
        current_hex = get_hex(current_rgb)
        response_data = set_color_data(current_hex)

        print(f"Color Swatches AFTER to pass to JSON: {color_swatches}")

        # Return json to javascript function which will find color-swatch element and update the background color
        return jsonify(response_data)

    except Exception as e:
         print(f"Exception in get pixel color: {e}")
         return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5001)