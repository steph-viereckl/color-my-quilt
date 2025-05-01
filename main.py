# --------------- Imports --------------------#

from pprint import pprint
from flask import Flask, jsonify, render_template, request, send_file, redirect, url_for
from flask_bootstrap import Bootstrap5
from networkx.algorithms.bipartite.basic import color
from pyscreeze import pixel
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO
import pyautogui
import os
import pyscreeze
import pandas
from static.assets.colors import color_chart
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from fabric_bot import FabricScraper
# ------------------- Constants and Initial Config -----------------#

# TODO How to let people upload photos but not store on our server?
UPLOAD_FOLDER = "static/uploads"
COLORS_FILE_PATH = 'static/assets/colors.csv'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Bootstrap5(app)

current_file = None
hex_color = "#fcba03"
color_to_update = 1 # Keeps track of which swatch box is outlined in red
color_swatches = {}
show_hex = False

# TODO need to think about how to organize so we always get the color file but don't always update it
fabric_scraper = FabricScraper()
colors_data_frame = pandas.read_csv(COLORS_FILE_PATH, index_col=0)

# ------------------- Helper Methods -----------------#

def format_hex(rgb_color):
    return '#{:02x}{:02x}{:02x}'.format(rgb_color[0], rgb_color[1], rgb_color[2])

def format_rbg(rgb_color):

    return [rgb_color[0], rgb_color[1], rgb_color[2]]
    # return f"rgb({rgb_color[0]},{rgb_color[1]},{rgb_color[2]})"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def set_color_data(hex, rgb):
    print(f"Set color data for: {color}")
    global color_swatches
    global color_to_update

    # Dynamically create key to set hex color
    color_swatches[color_to_update] = {
        "hex": hex,
        "rgb": rgb
    }

    # If the color number is less than 5, increase by 1 so the next value in the set of 5 can be updated
    if color_to_update < 5:
        color_to_update += 1
    # If the color number is 5, then restart from the beginning
    else:
        color_to_update = 1

    # Pass updated color swatches and the current color
    return {'color_swatches': color_swatches, 'next_color': color_to_update}

def reset_color_swatch():
    global color_swatches
    global color_to_update

    color_to_update = 1
    color_swatches = color_swatches = {
        1: {"hex": "#fffff", "rgb": [0, 0, 0]},
        2: {"hex": "#fffff", "rgb": [0, 0, 0]},
        3: {"hex": "#fffff", "rgb": [0, 0, 0]},
        4: {"hex": "#fffff", "rgb": [0, 0, 0]},
        5: {"hex": "#fffff", "rgb": [0, 0, 0]},
    }

def find_color_match(red, green, blue):

    print("find_color_match")
    # rgb from Selected Image
    selected_rgb = sRGBColor(red, green, blue)
    # Convert from RGB to Lab Color Space
    selected_lab_color = convert_color(selected_rgb, LabColor)

    for fabric in colors_data_frame:

        fabric_red = color_chart[fabric]["red"]
        fabric_green = color_chart[fabric]["green"]
        fabric_blue = color_chart[fabric]["blue"]
        fabric_rgb = sRGBColor(fabric_red, fabric_green, fabric_blue)
        # Convert from RGB to Lab Color Space
        fabric_lab_color = convert_color(fabric_rgb, LabColor)

        # Find the color difference
        delta_e = delta_e_cie2000(selected_lab_color, fabric_lab_color);
        print(f"Color difference is: {delta_e}")

        if delta_e < 20:
            print(f"Color match for {fabric}!")
            return fabric

    return None

# ------------------- URL Methods -----------------#

@app.route("/")
def home():
    reset_color_swatch()
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
        pixel_rgb = pyautogui.pixel(new_x, new_y)

        # Format so hex is "#FFFFFF" and rgb is [10,20,30]
        formatted_hex = format_hex(pixel_rgb)
        formatted_rgb = format_rbg(pixel_rgb)
        response_data = set_color_data(formatted_hex, formatted_rgb)
        # TODO: Need to allow toggle of rgb to hex

        print(f"Color Swatches AFTER to pass to JSON: {color_swatches}")
        print(f"response data: {response_data}")

        # Return json to javascript function which will find color-swatch element and update the background color
        return jsonify(response_data)

    except Exception as e:
         print(f"Exception in get pixel color: {e}")
         return jsonify({'error': str(e)})

@app.route('/update_current_color', methods=['POST'])
def update_current_color():
    """Upon clicking color swatch html, update the 'selected' color

    In order to keep track of the current color, update the global variable and pass back
    new current color so that the html can be updated
    """

    try:
        global color_to_update

        data = request.get_json()
        color_to_update = int(data["selected_swatch"])
        response_data = {'color_swatches': color_swatches, 'next_color': color_to_update}

        return jsonify(response_data)

    except Exception as e:
         print(f"Exception in get pixel color: {e}")
         return jsonify({'error': str(e)})


@app.route('/get_fabric_match', methods=['POST'])
def get_fabric_match():
    """.....

    """

    try:
        global color_to_update

        print("get fabric")
        print(f"color_to_update: {color_to_update}")
        print(f"color_swatches: {color_swatches}")

        current_color = color_swatches[color_to_update]
        print(f"current_color: {current_color}")


        color_match = find_color_match(current_color["rgb"][0], current_color["rgb"][1], current_color["rgb"][2])
        color_details = color_chart[color_match]
        print(f"color_match: {color_match}")
        print(f"color_details: {color_details}")

        # https://www.robertkaufman.com/fabrics/kona_cotton/?cotton&solids#products
        # TODO: Need to test that we are passing the correct details

        # Pass the user selected rbg value and see if there is a color match
        file_path = f"https://www.robertkaufman.com/assets/fabric/thumbs/{color_details["code"]}.jpg"
        print(f"file_path: {file_path}")

        # TODO: Need to add more colors to the color tiles... can I scrape color tiles and get pixel color?
        # And/Or maybe this should be a page on the website to drive traffic

        response_data = {'path': file_path, 'name': color_match}

        return response_data
    except Exception as e:
         print(f"Exception in get pixel color: {e}")
         return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5001)