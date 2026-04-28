import requests

query = "Data engineering"
url = f"https://openlibrary.org/search.json?q={query.replace(' ', '+')}"

response = requests.get(url)
data = response.json()

books = []

for book in data['docs']:
    #  print(f"Title: {book.get('title', 'N/A')}")
    #  print(f"Author: {', '.join(book.get('author_name', ['N/A']))}")
    #  print(f"First Published: {book.get('first_publish_year', 'N/A')}")
    #  print("-" * 40)

    books.append({
        'title': book.get('title', 'N/A'),
        'author': ', '.join(book.get('author_name', ['N/A'])),
        'first_publish_year': book.get('first_publish_year', 'N/A')
    }) 

for book in books:
    print (book)
    # print(f"Title: {book['title']}")
    # print(f"Author: {book['author']}")
    # print(f"First Published: {book['first_publish_year']}")
    print("-" * 40)