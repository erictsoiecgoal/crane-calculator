import base64

from flask import Flask, send_file, request, jsonify
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def plot_crane(boom_length, boom_angle_rad, boom_angle_deg):
    crane_x, crane_y = 0, 0
    boom_x = boom_length * np.cos(boom_angle_rad)
    boom_y = boom_length * np.sin(boom_angle_rad)

    plt.figure(figsize=(8, 6))
    plt.plot([crane_x, boom_x], [crane_y, boom_y], color='blue', linewidth=2, label='Boom')
    plt.scatter(crane_x, crane_y, color='red', s=100, label='Crane')
    plt.text(boom_x / 2, boom_y / 2, f'{boom_angle_deg:.1f}°', fontsize=12, color='black')

    plt.xlim(-1, boom_length + 1)
    plt.ylim(-1, boom_length + 1)
    plt.axhline(0, color='black', linewidth=0.5, ls='--')
    plt.axvline(0, color='black', linewidth=0.5, ls='--')
    plt.title('Crane Boom Diagram')
    plt.xlabel('X (Horizontal)')
    plt.ylabel('Y (Vertical)')
    plt.grid()
    plt.legend()

    # Save the figure to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()  # Close the figure to free memory

    base64_str = base64.b64encode(img.getvalue()).decode('utf-8')
    return base64_str
    # return img


@app.route('/plot_crane', methods=['POST'])
def plot_crane_service():
    data = request.json
    boomLength = data.get('boomLength')
    boomAngleRad = data.get('boomAngleRad')
    boomAngleDeg = data.get('boomAngleDeg')

    if boomLength is None or boomAngleRad is None or boomAngleDeg is None:
        return {"error": "Missing"}, 400

    # img = plot_crane(boomLength, boomAngleRad, boomAngleDeg)
    # return send_file(img, mimetype='image/png')
    base64_image = plot_crane(boomLength, boomAngleRad, boomAngleDeg)
    return jsonify({"image": base64_image})


@app.route('/plot_crane_img', methods=['POST'])
def plot_crane_service_img():
    data = request.json
    boomLength = data.get('boomLength')
    boomAngleRad = data.get('boomAngleRad')
    boomAngleDeg = data.get('boomAngleDeg')

    if boomLength is None or boomAngleRad is None or boomAngleDeg is None:
        return {"error": "Missing"}, 400

    base64_image = plot_crane(boomLength, boomAngleRad, boomAngleDeg)
    img = base64.b64decode(base64_image)
    image_io = io.BytesIO(img)

    # Return the image as a PNG file
    return send_file(image_io, mimetype='image/png', as_attachment=True, download_name='image.png')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
