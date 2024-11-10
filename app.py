from flask import Flask, jsonify, request
import requests
from googletrans import Translator
from flask_cors import CORS
import socket
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

# Configurar CORS para permitir solo el dominio específico
trusted_origin = "https://frontbibliomuni.onrender.com"
CORS(app, resources={r"/*": {"origins": [trusted_origin]}})

def get_book_data_by_isbn(isbn):
    url = (
        f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    )
    response = requests.get(url)

    if response.status_code == 200:
        book_data = response.json()
        if book_data:
            key = f"ISBN:{isbn}"
            if key in book_data:
                book_info = book_data[key]
                title = book_info.get("title", "No title available")
                authors = [author["name"] for author in book_info.get("authors", [])]
                publish_date = book_info.get(
                    "publish_date", "No publish date available"
                )

                # Traducir título y autores al español
                translator = Translator()
                title_es = translator.translate(title, dest="es").text
                authors_es = [
                    translator.translate(author, dest="es").text for author in authors
                ]

                return {
                    "title": title_es,
                    "authors": authors_es,
                    "publish_date": publish_date,
                }
            else:
                return {"error": "No data found for this ISBN."}
        else:
            return {"error": "No data found for this ISBN."}
    else:
        return {"error": f"Error fetching data. Status code: {response.status_code}"}

@app.route("/api/book", methods=["GET"])
def get_book():
    isbn = request.args.get("isbn")
    if not isbn:
        return jsonify({"error": "Please provide an ISBN"}), 400

    book_data = get_book_data_by_isbn(isbn)
    return jsonify(book_data)

if __name__ == "__main__":
    _port = os.getenv("PORT", 5000)  # Usa 5000 como puerto predeterminado si no está en el .env
    _host = os.getenv("HOST", "0.0.0.0")  # Usa 0.0.0.0 como host predeterminado
    ip_address = socket.gethostbyname(socket.gethostname())
    print(f"Servidor Flask corriendo en http://{ip_address}:{_port}")
    app.run(debug=False, host=_host, port=int(_port))
