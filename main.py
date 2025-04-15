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


UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Bootstrap5(app)

current_file = None
hex_color = "#fcba03"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    print("Running the / Method")
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

        return render_template("index.html", filename=current_file, hex_color=hex_color)

    return 'Invalid file type'

# Frontend (HTML/JavaScript):
# Create an HTML page that displays content.
# Add an event listener (e.g., onclick) to capture mouse clicks.
# When a click occurs, use JavaScript to get the mouse coordinates.
# Send these coordinates to the Python backend using an AJAX request.

def get_hex(rgb_color):
    return '#{:02x}{:02x}{:02x}'.format(rgb_color[0], rgb_color[1], rgb_color[2])


# On mouse click, get hex color
@app.route('/get_pixel_color', methods=['POST', 'GET'])
def get_pixel_color():
    print("Running the get_pixel_color")

    data = request.get_json()
    x = data['x']
    y = data['y']
    pixel_ratio = data['pixel_ratio']
    browser_bar_height = data['browser_bar_height']

    try:

        # When using pixel() directly, pyautogui was including the chrome browser bar
        # new_buffer = (browser_bar_height + 40) * pixel_ratio # The pixel() method is including the top chrome url/bookmarks bar :(
        # new_x = x * pixel_ratio
        # new_y = (y * pixel_ratio) + new_buffer
        # rgb_from_pixel = pyautogui.pixel(new_x, new_y)
        # current_hex = get_hex(rgb_from_pixel)

        # The pixel() method is expecting the chrome browser bar to be included in the x,y coordiantes
        mouse_x = pyautogui.position()[0] * pixel_ratio
        mouse_y = pyautogui.position()[1] * pixel_ratio
        mouse_rgb = pyautogui.pixel(mouse_x, mouse_y)
        mouse_hex = get_hex(mouse_rgb)

        print(f"Pyautogui x: {mouse_x}, y: {mouse_y}")

        data = {'new_hex_color': current_hex, 'mouse_hex_color': mouse_hex}
        return jsonify(data)



        # TODO This isn't updating the current color on the page
        # return render_template("index.html", filename=current_file, hex_color="#ffffff")
        # return redirect(url_for("home", filename=current_file, hex_color=hex_color))

    except Exception as e:
         print(f"Exception: {e}")
         return jsonify({'error': str(e)})

# Backend (Python):
# Set up a route in your Flask or Django application to receive the coordinates.
# Use pyautogui.pixel(x, y) to get the RGB color value of the pixel at the received coordinates.
# Send the color value back to the frontend as a response.

# Frontend (JavaScript):
# Process the response from the backend.
# Display the pixel color (e.g., as text or by changing the background color of an element).

if __name__ == '__main__':
    app.run(debug=True, port=5001)