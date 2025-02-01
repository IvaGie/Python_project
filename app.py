from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import numpy as np
import imageio.v2 as imageio

app = Flask(__name__)

# Nastavení složky pro nahrávání souborů
app.config["UPLOAD_FOLDER"] = "static/uploads"  # Složka pro nahrané obrázky
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Cesta k původnímu obrázku a aktuálně zpracovávanému obrázku
original_image_path = os.path.join(app.config["UPLOAD_FOLDER"], "original.jpg")
current_image_path = os.path.join(app.config["UPLOAD_FOLDER"], "current.jpg")

@app.route('/')
def home():
    return render_template("index.html")

def apply_negative(img_array):
    return 255 - img_array

def is_blackAndWhite(img_array):
    if len(img_array.shape) == 2:
        return True
    if img_array.shape[2] == 3:
        if np.all(img_array[:, :, 0] == img_array[:, :, 1]) and np.all(img_array[:, :, 1] == img_array[:, :, 2]):
            return True
    return False

def convert_to_lighter(img_array, percent_lighter=20):
    increase = img_array * (percent_lighter / 100)
    lightened = np.clip(img_array + increase, 0, 255)
    return lightened.astype(np.uint8)

def convert_to_darker(img_array, percent_darker=20):
    decrease = img_array * (percent_darker / 100)
    darkened = np.clip(img_array - decrease, 0, 255)
    return darkened.astype(np.uint8)

def make_smaller(img_array):
    if is_blackAndWhite(img_array):
        return img_array[::2, ::2]
    else:
        red_channel = img_array[::2, ::2, 0]
        green_channel = img_array[::2, ::2, 1]
        blue_channel = img_array[::2, ::2, 2]
        return np.stack([red_channel, green_channel, blue_channel], axis=-1)

@app.route("/upload", methods=["POST"])
def upload_file():
    global original_image_path, current_image_path
    if "file" not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})

    # Uložení původního obrázku
    file.save(original_image_path)
    # Původní obrázek nastavíme jako aktuální obrázek pro aplikaci filtrů
    imageio.imwrite(current_image_path, imageio.imread(original_image_path))

    return jsonify({"image_url": f"/static/uploads/{os.path.basename(original_image_path)}"})

@app.route("/filter/<filter_type>")
def apply_filter(filter_type):
    global current_image_path

    # Pokud není obrázek k dispozici, vrátíme chybu
    if not os.path.exists(current_image_path):
        return jsonify({"error": "No uploaded image"}), 400

    img_array = imageio.imread(current_image_path)

    # Získání procentuální hodnoty z query parametru
    percent = request.args.get("percent", default=20, type=int)

    # Aplikujeme příslušný filtr na aktuální obrázek
    if filter_type == "negative":
        img_array = apply_negative(img_array)
    elif filter_type == "lighter":
        img_array = convert_to_lighter(img_array, percent)
    elif filter_type == "darker":
        img_array = convert_to_darker(img_array, percent)
    elif filter_type == "smaller":
        img_array = make_smaller(img_array)
    else:
        return jsonify({"error": "Unknown filter"}), 400

    # Uložíme aktuální obrázek po aplikaci filtru
    imageio.imwrite(current_image_path, img_array)

    return jsonify({"image_url": f"/static/uploads/{os.path.basename(current_image_path)}"})

if __name__ == "__main__":
    app.run(debug=True)
