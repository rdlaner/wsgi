import re

import traceback
from bookdb import BookDB

DB = BookDB()
DEFAULT = "No value set"


def book(book_id):
    title_info = DB.title_info(book_id)

    try:
        body = (f"<h1>{title_info['title']}</h1>"
                f"<BR>"
                f"<table>"
                    f"<tr><th>Author:</th><td>{title_info['author']}</td></tr>"
                    f"<tr><th>Publisher:</th><td>{title_info['publisher']}</td></tr>"
                    f"<tr><th>ISBN:</th><td>{title_info['isbn']}</td></tr>"
                f"</table>"
                f"<a href='/'>Home</a>")
    except TypeError:
        raise NameError

    return body


def books():
    all_books = DB.titles()
    book_template = "<li><a href='/book/{id}'>{title}</a></li>"
    body = ["<h1>My Bookshelf</h1>", "<ul>"]

    for book in all_books:
        body.append(book_template.format(**book))
    body.append("</ul>")

    return "\n".join(body)


def resolve_path(path):
    funcs = {'': books,
             "book": book}

    path = path.strip("/").split("/")
    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    try:
        func, args = resolve_path(environ.get("PATH_INFO", DEFAULT))
        body = func(*args)
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    else:
        status = "200 OK"
    finally:
        headers = [('Content-type', 'text/html')]
        start_response(status, headers)

    return [f"<h1>{body}</h1>".encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
