class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def __repr__(self):
        return (f"User {self.name}, email: {self.email}, "
                f"books read: {len(self.books)}")

    def __eq__(self, other):
        return self.name == other.name and self.email == other.email

    def get_email(self):
        return self.email

    def change_email(self, email):
        if validate_email(email):
            self.email = email
            print(f"{self.name}'s email has been updated to {self.email}")

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        total_ratings = 0
        for rating in self.books.values():
            if rating is not None:
                total_ratings += rating
        return total_ratings / len(self.books)


class Book:
    def __init__(self, title, isbn, price):
        self.title = title
        self.isbn = isbn
        self.price = price
        self.ratings = []

    def __repr__(self):
        return self.title

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __eq__(self, other):
        return self.title == other.title and self.isbn == other.isbn

    def __getitem__(self, key):
        return key

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print(f"{self.title}'s ISBN has been changed to {self.isbn}")

    def get_price(self):
        return self.price

    def set_price(self, new_price):
        self.price = new_price
        print(F"{self.title}'s price has been changed to {self.price}")

    def add_rating(self, rating):
        if rating is not None and 0 <= rating <= 4:
            self.ratings.append(rating)
        else:
            print("Invalid Rating")

    def get_average_rating(self):
        total_ratings = 0
        for rating in self.ratings:
            total_ratings += rating
        return total_ratings / len(self.ratings)


class Fiction(Book):
    def __init__(self, title, author, isbn, price):
        super().__init__(title, isbn, price)
        self.author = author

    def __repr__(self):
        return f"{self.title} by {self.author}"

    def get_author(self):
        return self.author


class NonFiction(Book):
    def __init__(self, title, subject, level, isbn, price):
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level

    def __repr__(self):
        return f"{self.title}, a {self.level} manual on {self.subject}"

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level


class TomeRater:
    def __init__(self):
        self.users = {}
        self.books = {}

    def __repr__(self):
        return f"TomeRater: {len(self.users)} users, {len(self.books)} books."

    def __eq__(self, other):
        return (self.users.items() == other.users.items()
                and self.books.items() == other.books.items())

    def create_book(self, title, isbn, price):
        return Book(title, isbn, price)

    def create_novel(self, title, author, isbn, price):
        return Fiction(title, author, isbn, price)

    def create_non_fiction(self, title, subject, level, isbn, price):
        return NonFiction(title, subject, level, isbn, price)

    def add_book_to_user(self, book, email, rating=None):
        # Check if this user exists
        if email in self.users:
            self.users[email].read_book(book, rating)
            book.add_rating(rating)
            # If the book is in the catalog, add 1 to the read count
            if book in self.books:
                self.books[book] += 1
            else:
                # If the new book's ISBN is unique, add it to the catalog
                if all(book.isbn != books.isbn for books in self.books):
                    self.books[book] = 1
                else:
                    print(f"ISBN {book.isbn} already exists in catalog")
        else:
            print(f"No user with email {email}")

    def add_user(self, name, email, user_books=None):
        if validate_email(email):
            if email not in self.users:
                self.users[email] = User(name, email)
                print("user added")
                if user_books:
                    for book in user_books:
                        self.add_book_to_user(book, email, rating=None)
            else:
                print("User already exists")

    # Analysis methods
    def print_catalog(self):
        for book, rating in self.books.items():
            print(book, rating)

    def print_users(self):
        for user in self.users:
            print(user)

    def most_read_book(self):
        books_sorted = sorted(self.books.items(),
                              key=lambda book: book[1])
        return books_sorted[-1]

    def highest_rated_book(self):
        books_sorted = sorted(self.books,
                              key=lambda book: book.get_average_rating())
        return books_sorted[-1]

    def most_positive_user(self):
        users_sorted = sorted(self.users.items(),
                              key=lambda user: user[1].get_average_rating())
        return users_sorted[-1]

    def get_n_most_read_books(self, n):
        books_sorted = sorted(self.books.items(),
                              key=lambda book: book[1],
                              reverse=True)
        return books_sorted[:n]

    def get_n_most_prolific_readers(self, n):
        users_sorted = sorted(self.users.items(),
                              key=lambda user: len(user[1].books),
                              reverse=True)
        return users_sorted[:n]

    def get_n_most_expensive_books(self, n):
        books_sorted = sorted(self.books,
                              key=lambda book: book.price,
                              reverse=True)
        return books_sorted[:n]

    def get_worth_of_user(self, user_email):
        total_spent = 0
        for book in self.users[user_email].books:
            total_spent += book.price
        return total_spent


# This function should be developed and used with different objects
def validate_email(email):
    suffixes = [".com", ".edu", ".org"]
    if "@" in email and any(string in email for string in suffixes):
        return True
    else:
        print("Invalid email")
        return False
