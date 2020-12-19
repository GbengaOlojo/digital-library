class Error(Exception):
    pass

class BookDoesNotExist(Error):
    def __init__(self, book_id):
        self.book_id = book_id

    def __str__(self):
        return f"invalid Book ID: {self.book_id}"

class BookNotAvailable(Error):
    def __init__(self, book_title, book_id):
        self.book_title = book_title
        self.book_id = book_id
    
    def __str__(self):
        return f'Book not available: {self.book_title} - {self.book_id}'


class UserReantalConflictError(Error):
    def __init__(self, book_instance):
        self.book_instance = book_instance

    def __str__(self):
        return f' user rental record conflicts with running user. Book Instance: {self.book_instance}'