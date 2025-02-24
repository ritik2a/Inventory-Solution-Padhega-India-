def clean_isbn(isbn):
    # Example: Remove non-numeric characters
    return ''.join(filter(str.isdigit, str(isbn)))

def clean_title(title):
    # Example: Title case the book title
    return str(title).title()
