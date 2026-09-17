## This module contains the user interface for the library system. 
# It allows users to search for books, borrow books, and return books.

## Import the necessary functions from the admin module. 
# Replace "function_name1" with the actual function names you want to import.

from admin import (
    load_library,
    save_library,
    find_book
)



## Search books by category.
## This function should return book IDs that match the given category.
def books_in_category(
    books,
    category
):
    category = category.strip().lower()

    matching_ids = []

    for book_id, book in books.items():

        if (
            book["category"].lower()
            == category
        ):
            matching_ids.append(book_id)

    return matching_ids

    



## Search books by full or partial title.
## This function should return book IDs that match the given title or part of the title.
def search_by_title(
    books,
    search_text
):
    search_text = search_text.strip().lower()

    matching_ids = []

    for book_id, book in books.items():

        if (
            search_text
            in book["title"].lower()
        ):
            matching_ids.append(book_id)

    return matching_ids
    


## Create logic to let users borrow books.
## The function should check if the book is available or on loan, or if the borrower name is provided.
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not available, then return "NOT_AVAILABLE"
## If the book is successfully borrowed, then return "OK"
def borrow_book(
    books,
    loans,
    search_text,
    borrower
):
    book_id = find_book(
        books,
        search_text
    )

    if book_id is None:
        return "BOOK_NOT_FOUND"

    if (
        not borrower
        or not borrower.strip()
    ):
        return "EMPTY_NAME"

    if (
        not books[book_id]["available"]
    ):
        return "NOT_AVAILABLE"

    books[book_id]["available"] = False

    loans.append(
        {
            "book_id": book_id,
            "borrower": borrower
        }
    )

    return "OK"
    


## Create logic to let users return books.
## The function should check if the book is on loan, or if the borrower name is provided
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not on loan, then return "NOT_ON_LOAN"
## If the book is successfully returned, then return "OK"

def return_book(
    books,
    loans,
    book_title,
    borrower
):
    book_id = find_book(
        books,
        book_title
    )

    if book_id is None:
        return "BOOK_NOT_FOUND"

    if (
        not borrower
        or not borrower.strip()
    ):
        return "EMPTY_NAME"

    on_loan = any(
        loan["book_id"] == book_id
        for loan in loans
    )

    if not on_loan:
        return "NOT_ON_LOAN"

    loans[:] = [
        loan
        for loan in loans
        if loan["book_id"] != book_id
    ]

    books[book_id]["available"] = True

    return "OK"

    
    



## The main function that runs the user interface for the library system.
## The function must first load the library data from a JSON file, then display a menu for the user to select options.
## The options include searching for books by title or category, borrowing a book, returning a book, and exiting the program.
## When the user selects an option, the corresponding function is called to perform the action.
## The program continues to display the menu until the user chooses to exit, at which point the library data is saved back to the JSON file.
## The main function should also handle invalid selections by displaying an error message and prompting the user to select again.
def main():
    data = load_library("library.json")

    books = data["books"]
    loans = data["loans"]

    print("LIBRARY USER SYSTEM")

    while True:

        print("\nPlease select an option:")
        print("1. Search books by title")
        print("2. Search books by category")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            search_text = input(
                "Enter title to search: "
            )

            matching_ids = search_by_title(
                books,
                search_text
            )

            if matching_ids:

                print(
                    "Matching books found:"
                )

                for book_id in matching_ids:

                    print(
                        f"{book_id} | {books[book_id]['title']}"
                    )

            else:

                print(
                    "No books found with that title."
                )

        elif choice == "2":

            category = input(
                "Enter category to search: "
            )

            matching_ids = books_in_category(
                books,
                category
            )

            if matching_ids:

                print(
                    "Books found in that category:"
                )

                for book_id in matching_ids:

                    print(
                        f"{book_id} | {books[book_id]['title']}"
                    )

            else:

                print(
                    "No books found in that category."
                )

        elif choice == "3":

            search_text = input(
                "Enter book title, author, or ID: "
            )

            borrower = input(
                "Enter borrower name: "
            )

            result = borrow_book(
                books,
                loans,
                search_text,
                borrower
            )

            print(result)

        elif choice == "4":

            book_title = input(
                "Enter book title, author, or ID: "
            )

            borrower = input(
                "Enter borrower name: "
            )

            result = return_book(
                books,
                loans,
                book_title,
                borrower
            )

            print(result)

        elif choice == "5":

            save_library(
                data,
                "library.json"
            )

            print(
                "Library data saved. Goodbye!"
            )

            break

        else:

            print(
                "Invalid selection. Please try again."
            )


if __name__ == "__main__":
    main()
