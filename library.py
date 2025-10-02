import os
import json
from datetime import datetime, timedelta

class Book:
    id = 1
    Book_log = {}
    Total_books = 0
    file_path = "books.json"

    def __init__(self, title, author, genre, year, copies):
        self.__title = title
        self.__author = author
        self.__genre = genre
        self.__year = year
        self.__copies = copies
        # Use an integer key for in-memory Book_log
        Book.Book_log.update({
            Book.id: {
                'Title': self.__title,
                'Author': self.__author,
                'Genre': self.__genre,
                'Year': self.__year,
                'Copies': self.__copies
            }
        })
        Book.Total_books += self.__copies
        Book.id += 1
        # persist immediately
        Book.save_books()

    def __str__(self):
        return (f"We have {self.__copies} copies of {self.__title} by {self.__author} "
                f"in ({self.__year} - Genre: {self.__genre})")

    @classmethod
    def Books_amount(cls):
        return(f"We have a total amount of {cls.Total_books} books in the library.")

    @classmethod
    def save_books(cls):
        # JSON needs string keys; convert int keys to str for saving
        serializable = {str(k): v for k, v in cls.Book_log.items()}
        try:
            with open(cls.file_path, "w") as f:
                json.dump(serializable, f, indent=4)
        except Exception as e:
            print("Error saving books.json:", e)

    @classmethod
    def load_books(cls):
        cls.Book_log = {}
        cls.Total_books = 0
        cls.id = 1
        if os.path.exists(cls.file_path):
            try:
                with open(cls.file_path, "r") as f:
                    data = json.load(f)
                # handle if file contains a list or dict
                if isinstance(data, dict):
                    # convert keys back to ints when possible
                    normalized = {}
                    for k, v in data.items():
                        try:
                            ik = int(k)
                        except Exception:
                            # if key isn't integer-like, ignore or assign new id
                            ik = cls.id
                            cls.id += 1
                        # Ensure we have expected fields and consistent keys
                        # Accept either lower-case keys or capitalized ones
                        title = v.get('Title') or v.get('title') or "Unknown"
                        author = v.get('Author') or v.get('author') or "Unknown"
                        genre = v.get('Genre') or v.get('genre') or ""
                        year = v.get('Year') or v.get('year') or 0
                        copies = v.get('Copies')
                        if copies is None:
                            copies = v.get('copies', 0)
                        # normalize into the expected shape
                        normalized[ik] = {
                            'Title': title,
                            'Author': author,
                            'Genre': genre,
                            'Year': year,
                            'Copies': copies
                        }
                    cls.Book_log = normalized
                    if cls.Book_log:
                        cls.id = max(cls.Book_log.keys()) + 1
                        cls.Total_books = sum(int(b.get('Copies', 0) or 0) for b in cls.Book_log.values())
                else:
                    # unexpected format (list...), ignore file (start fresh)
                    cls.Book_log = {}
            except (json.JSONDecodeError, ValueError):
                # corrupted file — ignore and start fresh
                cls.Book_log = {}
        # if file missing or empty, we leave Book_log empty; defaults will be added when viewing

class Library:
    def add_book(self, title, author, genre, year, copies):
        Book(title, author, genre, year, copies)

    def view_books(self):
        if not Book.Book_log:
            # add defaults only when viewing if file had nothing
            self._add_default_books_if_empty()
        if not Book.Book_log:
            print("No books available.")
        else:
            numbering = 1
            print(f"{'-'*85}LIST OF BOOKS{'-'*85}")
            print('-'*140)
            print("{:^10}|{:^45}|{:^30}|{:^10}|{:^10}".format('S/N','TITLE','AUTHOR','YEAR','COPIES'))
            print('-'*140)
            for key, value in Book.Book_log.items():
                print("{:^10}|{:^45}|{:^30}|{:^20}|{:^10}".format(numbering, value['Title'], value['Author'], value['Year'], value['Copies']))
                numbering += 1

    def _add_default_books_if_empty(self):
        if not Book.Book_log:
            # only add defaults here — matches your previous seed list
            Book.Book_log.update({
                Book.id: {"Title": "The Great Gatsby", "Author": "F. Scott Fitzgerald", "Genre": "Classic", "Year": 1925, "Copies": 10}
            })
            Book.Total_books += 10
            Book.id += 1

            Book.Book_log.update({
                Book.id: {"Title": "Becoming", "Author": "Michelle Obama", "Genre": "Biography", "Year": 2018, "Copies": 20}
            })
            Book.Total_books += 20
            Book.id += 1

            Book.Book_log.update({
                Book.id: {"Title": "Educated", "Author": "Tara Westover", "Genre": "Memoir", "Year": 2018, "Copies": 15}
            })
            Book.Total_books += 15
            Book.id += 1

            Book.save_books()

    def search_books(self):
        query = input("what do you search by(title,author,genre,year): ").strip().lower()
        if query == "title":
            title = input("Enter the book title: ").strip().lower()
            result = [value['Title'].lower() for key,value in Book.Book_log.items()]
            if title in result:
                header = f'LIST OF BOOKS TITLED {title.upper()}'
                print(f"{'-'*(len(header)//2)}{header}{'-'*(len(header)//2)}")
                print('-'*160)
                print("{:^10}|{:^45}|{:^30}|{:^20}|{:^10}|{:^10}".format('S/N','TITLE','AUTHOR','GENRE','YEAR','COPIES'))
                print('-'*160)
                numbering = 1
                for key,value in Book.Book_log.items():
                    if value['Title'].lower() == title:
                        print("{:^10}|{:^45}|{:^30}|{:^20}|{:^10}|{:^10}".format(numbering,value['Title'],value['Author'],value['Genre'],value['Year'],value['Copies']))
                        numbering += 1
            else:
                print("Book not found.")
        elif query == "author":
            author = input("Enter the author's name:").strip().lower()
            result = [value['Author'].lower() for key, value in Book.Book_log.items()]
            if author in result:
                header = f'LIST OF BOOKS WRITTEN BY {author.upper()}'
                print(f"{'-' * (len(header) // 2)}{header}{'-'*(len(header)//2)}")
                print('-'*160)
                print("{:^10}|{:^45}|{:^30}|{:^20}|{:^10}|{:^10}".format('S/N','TITLE','AUTHOR','GENRE','YEAR','COPIES'))
                print('-'*160)
                numbering = 1
                for key,value in Book.Book_log.items():
                    if value ['Author'].lower() == author:
                        print("{:^10}|{:^45}|{:^30}|{:^20}|{:^10}|{:^10}".format(numbering,value['Title'],value['Author'],value['Genre'],value['Year'],value['Copies']))
                        numbering += 1
            else:
                print("Book not found")
        elif query == "genre":
            genre = input("Enter the book genre:").strip().lower()
            result = [value['Genre'].lower() for key, value in Book.Book_log.items()]
            if genre in result:
                header = f'LIST OF BOOKS WITH {genre.upper()} GENRE'
                print(f"{'-' * (len(header) // 2)}{header}{'-'*(len(header)//2)}")
                print('-'*160)
                print("{:^10}|{:^45}|{:^30}|{:^20}|{:^10}|{:^10}".format('S/N','TITLE','AUTHOR','GENRE','YEAR','COPIES'))
                print('-'*160)
                numbering = 1
                for key,value in Book.Book_log.items():
                    if value ['Genre'].lower() == genre:
                        print("{:^10}|{:^45}|{:^30}|{:^20}|{:^10}|{:^10}".format(numbering,value['Title'],value['Author'],value['Genre'],value['Year'],value['Copies']))
                        numbering += 1
            else:
                print("Book not found")
        elif query == "year":
            try:
                year = int(input("Enter the year in which the book was published:").strip())
            except ValueError:
                print("Invalid year.")
                return
            result = [value['Year'] for key, value in Book.Book_log.items()]
            if year in result:
                header = f'LIST OF BOOKS PUBLISHED IN THE YEAR {year}'
                print(f"{'-' * (len(header) // 2)}{header}{'-'*(len(header)//2)}")
                print('-'*160)
                print("{:^10}|{:^45}|{:^30}|{:^20}|{:^10}|{:^10}".format('S/N','TITLE','AUTHOR','GENRE','YEAR','COPIES'))
                print('-'*160)
                numbering = 1
                for key,value in Book.Book_log.items():
                    if value ['Year'] == year:
                        print("{:^10}|{:^45}|{:^30}|{:^20}|{:^10}|{:^10}".format(numbering,value['Title'],value['Author'],value['Genre'],value['Year'],value['Copies']))
                        numbering += 1
            else:
                print("Book not found")


    def delete_book_by_title(self, title):
        books_to_delete = [key for key, value in Book.Book_log.items() if value['Title'].lower() == title.lower()]
        if books_to_delete:
            for book_id in books_to_delete:
                # subtract copies from total
                copies = Book.Book_log[book_id].get('Copies', 0)
                try:
                    Book.Total_books -= int(copies)
                except Exception:
                    pass
                del Book.Book_log[book_id]
            Book.save_books()
            print(f"Books titled '{title}' have been deleted.")
        else:
            print(f"No books titled '{title}' found.")


class Member:
    Member_log = {}
    def __init__(self, name, member_id):
        self.__name = name
        self.__member_id= member_id
        Member.Member_log[self.__member_id] = self
    def get_name(self):
        return self.__name
    def get_student_id(self):
        return self.__member_id
    def __str__(self):
        return f"Student: {self.__name} (ID: {self.__member_id})"


class StudentRegistration:
    registered_students = {}
    borrowed_books = {}
    file_path = "students.json"

    @classmethod
    def load_students(cls):
        cls.registered_students = {}
        if os.path.exists(cls.file_path):
            try:
                with open(cls.file_path, "r") as f:
                    data = json.load(f)
                # expect data to be {id: name}
                for sid, name in data.items():
                    cls.registered_students[sid] = Member(name, sid)
            except (json.JSONDecodeError, ValueError):
                # corrupted file -> start empty
                cls.registered_students = {}

    @classmethod
    def save_students(cls):
        try:
            with open(cls.file_path, "w") as f:
                json.dump({sid: student.get_name() for sid, student in cls.registered_students.items()}, f, indent=4)
        except Exception as e:
            print("Error saving students.json:", e)

    @classmethod
    def add_default_students(cls):
        defaults = {
            "S101": "Alice Johnson",
            "S102": "Bob Smith",
            "S103": "Charlie Brown",
            "S104": "Diana Prince",
            "S105": "Ethan Hunt"
        }
        for sid, name in defaults.items():
            if sid not in cls.registered_students:
                cls.registered_students[sid] = Member(name, sid)
        cls.save_students()

    @classmethod
    def register_student(cls, name, student_id):
        if student_id in cls.registered_students:
            print(f"Student ID '{student_id}' is already registered.")
        else:
            student = Member(name, student_id)
            cls.registered_students[student_id] = student
            cls.save_students()
            print(f"Student '{name}' with ID '{student_id}' has been registered successfully.")

    @classmethod
    def list_students(cls):
        if not cls.registered_students:
            cls.add_default_students()
        print("\nRegistered Students:")
        print("-" * 40)
        print("{:^10} | {:^25}".format("Student ID", "Name"))
        print("-" * 40)
        for sid, student in cls.registered_students.items():
            print("{:^10} | {:^25}".format(sid, student.get_name()))

    @classmethod
    def delete_student_by_id(cls, student_id):
        if student_id in cls.registered_students:
            del cls.registered_students[student_id]
            cls.save_students()
            print(f"Student with ID '{student_id}' has been deleted.")
        else:
            print(f"No student found with ID '{student_id}'.")


    @classmethod
    def borrow_book(cls):
        student_id = input("Enter your student ID to borrow a book: ").strip()
        if student_id not in cls.registered_students:
            print("You are not registered. Please register first before borrowing books.")
            return

        book_title = input("Enter the title of the book you want to borrow: ").strip().lower()
        for book_id, details in Book.Book_log.items():
            if details['Title'].lower() == book_title:
                if int(details.get('Copies', 0)) > 0:
                    details['Copies'] = int(details.get('Copies', 0)) - 1
                    try:
                        Book.Total_books -= 1
                    except Exception:
                        pass
                    borrow_date = datetime.today()
                    due_date = borrow_date + timedelta(days=14)
                    if student_id not in cls.borrowed_books:
                        cls.borrowed_books[student_id] = []
                    cls.borrowed_books[student_id].append({
                        'Title': details['Title'],
                        'Borrowed': borrow_date.strftime("%Y-%m-%d"),
                        'Due': due_date.strftime("%Y-%m-%d")
                    })
                    Book.save_books()
                    print(f"You have borrowed '{details['Title']}'. Due date: {due_date.strftime('%Y-%m-%d')}")
                    return
                else:
                    print(f"'{details['Title']}' is currently out of stock.")
                    return
        print(f"Book titled '{book_title}' was not found.")

    @classmethod
    def return_book(cls):
        student_id = input("Enter your student ID to return a book: ").strip()
        if student_id not in cls.borrowed_books or not cls.borrowed_books[student_id]:
            print("You haven't borrowed any books.")
            return

        book_title = input("Enter the title of the book you're returning: ").strip().lower()
        for record in list(cls.borrowed_books[student_id]):
            if record['Title'].lower() == book_title:
                for book_id, details in Book.Book_log.items():
                    if details['Title'].lower() == book_title:
                        details['Copies'] = int(details.get('Copies', 0)) + 1
                        try:
                            Book.Total_books += 1
                        except Exception:
                            pass
                        break
                cls.borrowed_books[student_id].remove(record)
                Book.save_books()
                today = datetime.today()
                # record['Due'] stored as YYYY-MM-DD string
                try:
                    due_date = datetime.strptime(record['Due'], "%Y-%m-%d")
                except Exception:
                    due_date = today
                if today > due_date:
                    days_late = (today - due_date).days
                    print(f"Book returned late by {days_late} days.")
                else:
                    print("Book returned on time.")
                return
        print("You didn't borrow this book.")


# Library setup
library = Library()
# Load books from file (if any). Defaults are only added on view if file empty.
Book.load_books()
#

# Load students
StudentRegistration.load_students()

def main_menu():
    print("Welcome to the Library Management System")
    print('1. Total amount of books in the library:')
    print("2. Add Book")
    print("3. View Books")
    print("4. Search Books")
    print("5. Delete Book by Title")
    print("6. Register Student")
    print("7. List Students")
    print("8. Borrow Book")
    print("9. Return Book")
    print("10. Delete Student by ID")
    print("Type 'clear' to clear the screen.")

    

main_menu()
while True:
    choice = input("Enter your choice (1-9) or 'q' to quit: ").strip().lower()
    if choice == '1':
        print(Book.Books_amount())
    elif choice == '2':
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        genre = input("Enter book genre: ")
        year = int(input("Enter book year: "))
        copies = int(input("Enter number of copies: "))
        library.add_book(title, author, genre, year, copies)
    elif choice == '3':
        library.view_books()
    elif choice == '4':
        library.search_books()
    elif choice == '5':
        title = input("Enter the title of the book to delete: ")
        library.delete_book_by_title(title)
    elif choice == '6':
        name = input("Enter student name: ")
        student_id = input("Enter student ID: ")
        StudentRegistration.register_student(name, student_id)
    elif choice == '7':
        StudentRegistration.list_students()
    elif choice == '8':
        StudentRegistration.borrow_book()
    elif choice == '9':
        StudentRegistration.return_book()
    elif choice == '10':
        student_id = input("Enter student ID to delete: ")
        StudentRegistration.delete_student_by_id(student_id)

    elif choice == 'q':
        print("Exiting the Library Management System.")
        break
    elif choice == 'clear':
        os.system('cls')
        main_menu()
    else:
        print("Invalid choice. Please try again.")
