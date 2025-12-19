from flask import Flask, send_file, request
import io
import barcode
from barcode.writer import ImageWriter

app = Flask(__name__)

@app.route('/api/barcode')
def generate_barcode():
    # 1. Obtener el código
    code = request.args.get('code')
    if not code:
        return "Missing code parameter", 400

    try:
        # 2. Configurar el tipo de código de barras
        # Usamos 'code128' que es el estándar para vouchers
        EAN = barcode.get_barcode_class('code128')
        ean = EAN(code, writer=ImageWriter())
        
        # 3. Guardar en un buffer de memoria (indispensable para Render)
        fp = io.BytesIO()
        ean.write(fp)
        fp.seek(0)
        
        # 4. Retornar el archivo como imagen PNG
        return send_file(fp, mimetype='image/png')
        
    except Exception as e:
        return f"Error interno: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
