from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
import requests
import pandas

KAUFMAN_BASE_URL = "https://www.robertkaufman.com/"
KAUFMAN_ALL_PRODUCTS_URL = "https://www.robertkaufman.com/fabrics/kona_cotton/?cotton&solids&page=All#products"

# ============ Helper Methods ===============

class FabricScraper:

    def __init__(self):

        # ============ Get Driver ===============

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        # Instantiate browser of choice
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(KAUFMAN_ALL_PRODUCTS_URL)

        # self.wait = WebDriverWait(self.driver, 10)
        # Get the ui list where the tiles are stored
        fabric_list = self.driver.find_element(By.CLASS_NAME, "fabric-item-fabrics-list")
        # Get the li items
        fabric_tiles = fabric_list.find_elements(By.TAG_NAME, 'li')
        test_tiles = [fabric_tiles[5], fabric_tiles[10], fabric_tiles[15]]

        colors = {}

        # Loop through the li
        for tile in fabric_tiles:
        # for tile in test_tiles:

            tile_id = tile.get_attribute("id")
            tile_class= tile.get_attribute("class")
            fabric_code = tile_id[3:]

            if tile_id.startswith("li_K001") and tile_class != "available_later_product":

                img_src = tile.find_element(By.TAG_NAME, "img").get_attribute("src")
                img_url = f"{img_src}"
                fabric_name = tile.find_element(By.CLASS_NAME, "fabrics_yards_item_info").text.splitlines()[1]
                print(f"Getting data for {fabric_name}....")

                # Get the rgb color at (10, 10) coordinates (random coordinates
                fabric_rgb = self.get_pixel_color(img_url, 10, 10)

                # QUESTION: Would it be better to make this into a Python class?
                # I decided not to because I like having a key in the dictionary that I can access
                colors[fabric_name] = {
                    "code": fabric_code,
                    "img_url": img_url,
                    "red": fabric_rgb[0],
                    "green": fabric_rgb[1],
                    "blue": fabric_rgb[2]
                }

        print(f"Colors: {colors}")
        file_path = 'static/assets/colors.csv'

        pandas.DataFrame.from_dict(data=colors, orient='index').to_csv(file_path, header=False)


    def get_pixel_color(self, image_url, x, y):
        """
        Retrieves the RGB color of a pixel at given coordinates from an image URL.

        Args:
            image_url: The URL of the image.
            x: The x-coordinate of the pixel.
            y: The y-coordinate of the pixel.

        Returns:
            A tuple representing the RGB color of the pixel, or None if an error occurs.
        """
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            image = Image.open(BytesIO(response.content)).convert("RGB")
            width, height = image.size

            if 0 <= x < width and 0 <= y < height:
                return image.getpixel((x, y))
            else:
                return None  # Coordinates are out of bounds
        except requests.exceptions.RequestException as e:
            print(f"Error downloading image: {e}")
            return None
        except Exception as e:
            print(f"Error processing image: {e}")
            return None

fabric_scraper = FabricScraper()

