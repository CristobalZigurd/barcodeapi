# app.py (Flask)
# 1. Create a file named 'app.py'
# 2. Paste this code

from flask import Flask, send_file, request
import io
import barcode
from barcode.writer import ImageWriter

app = Flask(__name__)

@app.route('/api/barcode')
def generate_barcode():
    # Get code from URL query params
    code = request.args.get('code')
    if not code:
        return "Missing code", 400

    try:
        # Generate Code 128
        EAN = barcode.get_barcode_class('code128')
        ean = EAN(code, writer=ImageWriter())

        # Save to memory buffer (no file on disk)
        fp = io.BytesIO()
        ean.write(fp)
        fp.seek(0)

        # Return as Image (PNG)
        return send_file(fp, mimetype='image/png')

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)