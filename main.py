import argparse
import os
import sys
import time
from urllib.parse import urljoin
from urllib.parse import urlsplit

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from requests import ConnectionError
from requests import HTTPError

import json


def check_for_redirect(response):
    if response.status_code == 302:
        raise HTTPError


def get_generated_book(response, book_id):
    soup = BeautifulSoup(response.text, 'lxml')

    #  Parsing book's title

    books_tag = soup.select_one("h1")

    title_and_author = books_tag.text.split("\xa0 :: \xa0")
    books_title, books_author = title_and_author

    #  Parsing book's images

    books_image_part = soup.select_one("div.bookimage img")["src"]
    image_url = urljoin(response.url, books_image_part)

    # src for picture
    img_id = books_image_part.split("/")[2]
    split_img_id= img_id.split(".")
    src_img =str(book_id)+"."+books_title.strip()+"."+split_img_id[1]

    #  Parsing book's comments

    books_comments = soup.select("div.texts")
    comments = [comment.select_one("span.black").text for comment in
                books_comments]

    #  Parsing book's genres

    genres_selector = "span.d_book"
    books_genres = soup.select(genres_selector)
    for genre in books_genres:
        genres=genre.select_one("a")["title"].split("-")[0].split(",")


    generated_book = {
        "title": books_title.strip(),
        "author": books_author.strip(),
        "image": image_url,
        "comments": comments,
        "genre": genres,
        "book_id": book_id,
        "src_img": src_img
    }
    # print(generated_book)
    return generated_book


def save_book_in_json(books, filepath_to_json):
    json_filepath = os.path.join(filepath_to_json, "books.json")
    with open(json_filepath, "w", encoding='utf8') as my_file:
        json.dump(books, my_file, ensure_ascii=False,indent=4)


def download_txt(books_dictionary, filepath_to_text_directory, book_id):
    download_text_link = "https://tululu.org/txt.php"
    paylaod = {
        "id": book_id
    }

    text_response = requests.get(download_text_link, params=paylaod,
                                 allow_redirects=False)
    check_for_redirect(text_response)
    text_filepath = os.path.join(filepath_to_text_directory,
                                 f"{book_id}. {sanitize_filename(books_dictionary['title'])}")
    with open(f"{text_filepath}.txt", "w", encoding="utf-8") as file:
        file.write(text_response.text)


def download_img(filepath_to_image_directory, books_dictionary, book_id):
    image_response = requests.get(books_dictionary["image"])
    image_extension = urlsplit(books_dictionary["image"]).path.split(".")[1]
    image_filepath = os.path.join(filepath_to_image_directory,
                                  f"{book_id}.{books_dictionary['title']}.{image_extension}")

    with open(image_filepath, 'wb') as file:
        file.write(image_response.content)


def main():
    parser = argparse.ArgumentParser(
        description="script for parsing on-line lib")
    parser.add_argument("--start_id", "-s", help="?????????????????? ????????????????",
                        type=int, default=1)
    parser.add_argument("--end_id", "-e", help="K??????????????  ????????????????", type=int,
                        default=10)
    args = parser.parse_args()

    first_book_id = args.start_id
    last_book_id = args.end_id

    for book_id in range(first_book_id, last_book_id):
        try:
            check_for_redirect_link = f"https://tululu.org/b{book_id}/"
            response = requests.get(check_for_redirect_link,
                                    allow_redirects=False)
            check_for_redirect(response)

            response.raise_for_status()
            books_generated = get_generated_book(response, book_id)

            filepath_to_books = os.path.join("books")
            filepath_to_images = os.path.join("images")
            filepath_to_json = os.path.join("json")
            os.makedirs(filepath_to_books, exist_ok=True)
            os.makedirs(filepath_to_images, exist_ok=True)
            os.makedirs(filepath_to_json, exist_ok=True)
            download_txt(books_generated, filepath_to_books, book_id)
            download_img(filepath_to_images, books_generated, book_id)
            save_book_in_json(books_generated, filepath_to_json)


        except ConnectionError:
            print("???????????? ????????????????????", file=sys.stderr)
            sys.stdout = open('errors.txt', 'a', encoding='utf8')
            time.sleep(30)
        except requests.exceptions.HTTPError:
            print("???????????????? ???? ??????????????", response.url)
        except OSError:
            image_filepath = "https://tululu.org/images/nopic.gif"


if __name__ == '__main__':
    main()
