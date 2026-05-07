from flask import Flask, render_template_string, send_from_directory
import os
from zipfile import ZipFile

app = Flask(__name__)

# =========================
# AUTO-EXTRACT ZIP ASSETS
# =========================
ZIP_FILE = 'dns_brand_asset_pack_2023.zip'
ASSET_FOLDER = 'assets'

if not os.path.exists(ASSET_FOLDER):
    os.makedirs(ASSET_FOLDER, exist_ok=True)

    if os.path.exists(ZIP_FILE):
        with ZipFile(ZIP_FILE, 'r') as zip_ref:
            zip_ref.extractall(ASSET_FOLDER)

# =========================
# FIND IMAGE AUTOMATICALLY
# =========================
image_path = None

for root, dirs, files in os.walk(ASSET_FOLDER):
    for file in files:
        if file.endswith('.png'):
            image_path = os.path.join(root, file).replace('\\', '/')
            break

# =========================
# HTML TEMPLATE
# =========================
HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DNSTeam</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }

        body {
            background: #000;
            color: white;
            height: 100vh;
            overflow: hidden;
        }

        .container {
            display: flex;
            height: 100vh;
        }

        .left {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #111, #1a1a1a);
            position: relative;
        }

        .left img {
            width: 320px;
            max-width: 80%;
            filter: drop-shadow(0px 0px 25px rgba(255,255,255,0.25));
            position: absolute;
            top: 90px;
        }

        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }

        .left-text {
            position: absolute;
            top: 460px;
            text-align: center;
            width: 100%;
            padding: 20px;
        }

        .left-text h1 {
            font-size: 42px;
            margin-bottom: 10px;
        }

        .left-text p {
            font-size: 28px;
            font-weight: bold;
            background: linear-gradient(90deg, #ff0080, #7928ca);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            max-width: 650px;
            margin: auto;
            line-height: 1.4;
        }

        .right {
            width: 420px;
            background: #121212;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 30px;
        }

        .login-box {
            width: 100%;
        }

        .logo {
            font-size: 42px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 40px;
            background: linear-gradient(90deg, #ff0080, #7928ca);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        input {
            width: 100%;
            padding: 14px;
            margin-bottom: 15px;
            border: none;
            border-radius: 10px;
            background: #1f1f1f;
            color: white;
            font-size: 15px;
        }

        input:focus {
            outline: 2px solid #7928ca;
        }

        button {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 10px;
            background: linear-gradient(90deg, #ff0080, #7928ca);
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }

        button:hover {
            transform: scale(1.02);
            opacity: 0.95;
        }

        .footer {
            margin-top: 20px;
            text-align: center;
            color: #888;
            font-size: 13px;
        }

        @media(max-width: 900px) {
            .left {
                display: none;
            }

            .right {
                width: 100%;
            }
        }
    </style>
</head>
<body>

<div class="container">

    <div class="left">
        <img src="/{{ image_url }}" alt="Brand Logo">

        <div class="left-text">
            <h1>DNSTeam</h1>
            <p>See everyday moments from your close friends</p>
        </div>
    </div>

    <div class="right">
        <div class="login-box">
            <div class="logo">DNSTeam</div>

            <form>
                <input type="text" placeholder="Username">
                <input type="password" placeholder="Password">
                <button type="submit">Log In</button>
            </form>

            <div class="footer">
                Powered by DNSTeam Assets
            </div>
        </div>
    </div>

</div>

</body>
</html>
'''

# =========================
# ROUTES
# =========================
@app.route('/')
def home():
    return render_template_string(
        HTML,
        image_url=image_path
    )

@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory(ASSET_FOLDER, filename)

# =========================
# RUN
# =========================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
