# PhotoAlbum

## Назначение

Web-приложение **PhotoAlbum** предназначено для размещения в сети Интернет пользовательских фотографий. 

В базе уже есть несколько пользователей:

| Пользователь | e-mail | Пароль |
| ------------ | ------ | ------ |
| user1 | user1@localhost.ru | 1 |
| user2 | user2@localhost.ru | 1 |
| user3 | user3@localhost.ru | 1 |

## Системные требования

Работа приложения проверялась в **Python 3.9.1** под управлением операционной системы Windows 10 и Xubuntu 20.04.

Для корректной работы приложения необходимо установить следующие библиотеки:

- flask
  ```cmd
  pip install flask
  ```
- flask-wtf
  ```cmd
  pip install flask-wtf
  ```
- flask_login
  ```cmd
  pip install flask_login
  ```  
- flask_ckeditor
  ```cmd
  pip install flask_ckeditor
  ```
- PIL
  ```cmd
  pip install pillow
  ```
- sqlalchemy
  ```cmd
  pip install sqlalchemy
  ```


Смотри файл [requirements.txt](requirements.txt).

## Порядок сборки проекта в автономное приложение

**Запуск приложения:**

Для запуска приложения неоходимо установить все недостающие компоненты. После этого запустить файл **start.py**

**Известные проблемы:**

- Убедитесь, что установлен python последней версии
- При необходимости установите недостающие модули


## Что еще можно доделать

Много чего хотелось бы добавить, например:

- сделать настройки пользователя 
- нормальное создание миниатюр
- открытие изображений на текущей странице а не преход на новую страницу
- проверка почты при регистрации
- ... 



###P.S.

Персональный проект в рамках подготовки преподавателей второго года обучения ЯЛ.
