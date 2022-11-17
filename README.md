# Парсер книг с сайта tululu.org https://tululu.org/

## Запуск
 * Скачайте код
 * Установите зависимости командой 
 
     ```pip install -r requirements.txt```
 
## Работа со скриптом main.py

Для запуска скрипта main.py в консоль необходимо передать два аргумента :

     - номер первой скачиваемой книги  -s 7 
     - номер последней скачиваемой книги -e 45 
      
Скрипт скачает все книги от первой до последней.      
Аргументы по-умалочанию `-s 1` `-e 10`

## Пример ввода скрипта main.py в консоль 

`\library_parsing>python main.py -s 5 -e 45`

## Пример работы скрипта main.py
`\library_parsing>python main.py -s 5 -e 45`

Битая сслыка  https://tululu.org/txt.php?id=7 \
Битая сслыка  https://tululu.org/txt.php?id=14 \
Битая сслыка  https://tululu.org/txt.php?id=16 \
Битая сслыка  https://tululu.org/txt.php?id=17 \
Битая сслыка  https://tululu.org/txt.php?id=22 \
Битая сслыка  https://tululu.org/txt.php?id=23  

## Работа со скриптом  parse_tululu_category.py


Скрипт parse_tululu_category.py скачивает книги из категории: "Научная фантастика".

Настройки скрипта parse_tululu_category.py:

       --books_dir  - название для директории с книгами, по-умолчанию /books
       --image_dir  - название для директории с обложками, по-умолчанию /images
       --json_path  - название для директории с json-файлом, по-умолчанию /json
       --start_page - начальная страница, по-умолчанию  1
       --end_page   - конечная страница, по-умолчанию  701
       --skip_imgs  - отменить скачивание обложек
       --skip_txt   - отменить скачивание книг
     
## Пример ввода скрипта parse_tululu_category.py в консоль 

`python parse_tululu_category.py  --start_page 1 --end_page 25  --books_dir ski_fi_books  --image_dir ski_fi_images --json_path books_json`



## Пример parse_tululu_category.py
`library_parsing>python parse_tululu_category.py  --start_page 1 --end_page 25  --books_dir ski_fi_books  --image_dir ski_fi_images --json_path books_json`

Скачать не удалось https://tululu.org/b19738/ \
Скачать не удалось https://tululu.org/b19739/ \
Скачать не удалось https://tululu.org/b19741/ \
Скачать не удалось https://tululu.org/b19742/ \
Скачать не удалось https://tululu.org/b19743/ \
Скачать не удалось https://tululu.org/b19748/



 
## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков  https://dvmn.org.
