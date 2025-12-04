from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search_books():
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'error': 'No search query provided'})
    
    url = f"https://www.googleapis.com/books/v1/volumes"
    params = {
        'q': query,
        'maxResults': 20,
        'printType': 'books'
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        books = []
        for item in data.get('items', []):
            volume_info = item.get('volumeInfo', {})
            book = {
                'title': volume_info.get('title', 'No title'),
                'authors': volume_info.get('authors', ['Unknown']),
                'publishedDate': volume_info.get('publishedDate', ''),
                'description': volume_info.get('description', 'No description available.'),
                'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                'previewLink': volume_info.get('previewLink', ''),
                'infoLink': volume_info.get('infoLink', '')
            }
            books.append(book)
        
        return jsonify(books)
        
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)