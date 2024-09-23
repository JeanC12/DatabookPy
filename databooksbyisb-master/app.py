from flask import Flask, jsonify, request
import requests
from googletrans import Translator
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This line enables CORS for all routes on all origins


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
    app.run(debug=True)
