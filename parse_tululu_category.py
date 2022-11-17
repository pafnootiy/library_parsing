import argparse
import os
import sys
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from main import check_for_redirect
from main import download_img
from main import download_txt
from main import get_generated_book
from main import save_book_in_json


def get_books_link_parts(response):
    soup = BeautifulSoup(response.text, 'lxml')
    books_link_parts = soup.select("div.bookimage a[href]")
    return books_link_parts


def main():
    parser = argparse.ArgumentParser(
        description="script for parsing on-line lib")
    parser.add_argument('--books_dir', type=str, help='direction for books',
                        default="books")
    parser.add_argument('--image_dir', type=str, help='direction for items',
                        default="images")
    parser.add_argument('--json_path', type=str, help='direction for json',
                        default="json")
    parser.add_argument("--start_page", "-s", help="first page", type=int,
                        default=1)
    parser.add_argument("--end_page", "-e", help="last page", type=int,
                        default=7)
    parser.add_argument('--skip_imgs', action='store_true')
    parser.add_argument('--skip_txt', action='store_true')
    args = parser.parse_args()

    start_page = args.start_page
    end_page = args.end_page
    book_dir = args.books_dir
    img_dir = args.image_dir
    json_dir = args.json_path

    skip_images = args.skip_imgs
    skip_text = args.skip_txt

    filepath_to_books = os.path.join(book_dir)
    filepath_to_images = os.path.join(img_dir)
    filepath_to_json = os.path.join(json_dir)

    os.makedirs(filepath_to_books, exist_ok=True)
    os.makedirs(filepath_to_images, exist_ok=True)
    os.makedirs(filepath_to_json, exist_ok=True)
    books_details = []

    for page_id in range(start_page, end_page):
        try:
            sci_fi_collection_link = f"https://tululu.org/l55/{page_id}/"
            print("-->Страница с книгами", sci_fi_collection_link)
            book_page_response = requests.get(sci_fi_collection_link)

            check_for_redirect(book_page_response)
            book_page_response.raise_for_status()
            books_link_parts = get_books_link_parts(book_page_response)

            for link in books_link_parts:
                books_link = urljoin(sci_fi_collection_link, link["href"])
                print("Скачиваю книгу:", books_link)
                book_id = link["href"].split("/b")[1].replace("/", "")

                try:

                    books_link_response = requests.get(books_link)
                    check_for_redirect(books_link_response)
                    books_link_response.raise_for_status()
                    generated_book = get_generated_book(books_link_response,
                                                        book_id)
                    books_details.append(generated_book)

                    if not skip_images:
                        download_img(filepath_to_images, generated_book,
                                     book_id)
                    if not skip_text:
                        download_txt(generated_book, filepath_to_books,
                                     book_id)


                except requests.exceptions.HTTPError:
                    books_details.remove(generated_book)
                    
                    print("Скачать не удалось", books_link_response.url,
                              file=sys.stderr)



                except requests.exceptions.ConnectionError:
                    print("Ошибка соединения", file=sys.stderr)
                    sys.stdout = open('errors.txt', 'a', encoding='utf8')
                    time.sleep(10)
                except OSError:
                    image_filepath = "https://tululu.org/images/nopic.gif"
        except requests.exceptions.HTTPError:
            print("Скачать не удалось", sci_fi_collection_link,
                  file=sys.stderr)
        except requests.exceptions.ConnectionError:
            print("Ошибка соединения", file=sys.stderr)
            sys.stdout = open('errors.txt', 'a', encoding='utf8')
            time.sleep(10)

    # generated_book = get_generated_book(books_link_response,
    #                                     book_id)
    # books_details.append(generated_book)
    save_book_in_json(books_details, filepath_to_json)


if __name__ == '__main__':
    main()
