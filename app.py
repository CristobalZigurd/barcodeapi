from flask import Flask, send_file, request
import io
import barcode
from barcode.writer import ImageWriter

app = Flask(__name__)

@app.route('/api/barcode')
def generate_barcode():
    # Obtener el código de los parámetros de la URL
    code = request.args.get('code')
    if not code:
        return "Missing code", 400

    try:
        # Generar el código de barras en memoria
        EAN = barcode.get_barcode_class('code128')
        # ImageWriter genera el formato PNG
        ean = EAN(code, writer=ImageWriter())
        
        # Usamos un búfer de bytes para no escribir en el disco de Render
        fp = io.BytesIO()
        ean.write(fp)
        fp.seek(0) # Volver al inicio del archivo antes de enviar
        
        return send_file(fp, mimetype='image/png')
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
