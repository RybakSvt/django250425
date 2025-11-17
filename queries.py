import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# from test_app.models import (
#     Book,
#     UserProfile
# )


# try:
#     book = Book.objects.get(author="Leo Tolstoy")  # MultipleObjectsReturned
#     # book = Book.objects.get(id=999999999)  # DoesNotExist
#
#     print(book)
# except Book.DoesNotExist as err:
#     print("Нет такой книги", err)
# except Book.MultipleObjectsReturned as err:
#     print("Слишком много книг найдено", err)


# leo_books = Book.objects.filter(author="Leo Tolstoy")
#
# print(leo_books.query)
# print(leo_books)


# __contains == частичное совпадение с учётом регистра
# __icontains == частичное совпадение БЕЗ учёта регистра
# i == ignore_case

# leo_books = Book.objects.filter(title__contains="P")
#
# print(leo_books.query)
# print(leo_books)



# books = Book.objects.filter(id__in=[15, 280, 361])
#
# print(books.query)
#
# for b in books:
#     print(b.id, b.title)


# books = Book.objects.filter(pages__gt=500)
#
# print(books.query)
#
# for b in books:
#     print(b.id, b.title)


# filter(<field_name>__<lookups_name>)
# books = Book.objects.filter(published_date__gte="2020-01-01")
#
# print(books.query)
#
# for b in books:
#     print(b.id, b.published_date)


# books = Book.objects.filter(pages__isnull=True)
#
# print(books.query)
#
# for b in books:
#     print(b.id, b.published_date)


# books = Book.objects.filter(title__startswith="A")
#
# print(books.query)
#
# for b in books:
#     print(b.id, b.published_date)


# books = Book.objects.filter(pages__range=[<start>, <stop>])
# books = Book.objects.filter(pages__range=[500, 700])
#
# print(books.query)
#
# for b in books:
#     print(f"{b.id=}  -- {b.pages=}")


#
# books = Book.objects.filter(
#     pages__range=[500, 700],
#     published_date__gte='2020-01-01'
# )
#
# print(books.query)
#
# for b in books:
#     print(f"{b.id=}  -- {b.pages=}")



# =====================================================================

# from django.db.models import Q

# Q class

# OR - |
# AND - &
# NOT - ~

# data = Book.objects.filter(
#     Q(Q(author__startswith="Fyodor") | Q(author__startswith="Jack")) & Q(published_date__gte='2015-05-31')
# )
#
# print(data.query)
#
# for b in data:  # type: Book
#     print(f"{b.id=}  --  {b.author}  --  {b.published_date}")


# """
# SELECT
#     "books"."id",
#     "books"."title",
#     "books"."description",
#     "books"."author",
#     "books"."published_date",
#     "books"."pages"
# FROM "books"
# WHERE (
#           ("books"."author" LIKE Fyodor% ESCAPE '\'
#           OR "books"."author" LIKE Jack% ESCAPE '\'
#           )
#               AND "books"."published_date" >= 2015-05-31
#       )
# ORDER BY "books"."published_date" ASC
#
# """


# data = Book.objects.filter(
#     Q(
#         Q(author__startswith="Fyodor") | Q(Q(author__startswith="Jack") & ~Q(author__endswith="London"))
#     ) & Q(published_date__gte='2015-05-31')
# )
#
# print(data.query)
#
# for b in data:  # type: Book
#     print(f"{b.id=}  --  {b.author}  --  {b.published_date}")

from decimal import Decimal

# book = Book.objects.get(id=700)
#
# print("BEFORE:")
# print(book.is_bestseller)
# print(book.price)
#
#
# book.is_bestseller = True
# book.price = Decimal("189.97")
#
# book.save()
# print("AFTER:")
# print(book.is_bestseller)
# print(book.price)


# books = Book.objects.filter(
#     author__in=["Leo Tolstoy", "Fyodor Dostoevsky"]
# ).update(is_bestseller=True, price=Decimal("299.99"))
#


# from django.db.models import F
#
#
# books = Book.objects.filter(
#     author__in=["Leo Tolstoy", "Fyodor Dostoevsky"]
# ).update(discounted_price=F('price') * 0.80)



# book_to_delete = Book.objects.get(id=720)
#
#
# book_to_delete.delete()
#
#
#
# Book.objects.create()
# Book.objects.bulk_create()
# Book.objects.bulk_update()



# =====================================================
# New Lecture AGGREGATE && ANNOTATE
# =====================================================

from library.models import Book, Category, Borrow, User
from django.db.models import (
    Avg,
    Count,
    Min,
    Max, Q
)
from typing import Any

# Посчитать общее кол-во книг + средняя цена всех книг

# {} -> aggregate()

# aggregate_result: dict[str, Any] = Book.objects.aggregate(
#     books_count=Count('id'),
#     avg_books_price=Avg('price')
# )

# print(f"Общее кол-во всех книг в базе = ", aggregate_result['books_count'])
# print(f"Общее кол-во всех книг в базе = ", aggregate_result.get('books_count'))

# print(f"Средняя цена всех книг в базе = ", aggregate_result['avg_books_price'])
# print(f"Средняя цена всех книг в базе = ", aggregate_result.get('avg_books_price'))



# aggregate_result_min_max: dict[str, Any] = Book.objects.aggregate(
#     min_book_aprice=Min('price'),
#     max_book_price=Max('price')
# )
#
# print(aggregate_result_min_max)


# annotate()


# annotated_books_with_custom_field = Book.objects.values('author').annotate(
#     books_count=Count('id')
# ) # <QuerySet[{...}, ..., {...}]>

# print(annotated_books_with_custom_field.query)


# for obj in annotated_books_with_custom_field:
#     print(f"Автор: {obj.author}, кол-во книг = {obj.books_count}")


# for obj in annotated_books_with_custom_field:
#     print(f"Автор: {obj['author']}, кол-во книг = {obj['books_count']}")


# books_by_category = Category.objects.values('name_category').annotate(
#     books_count=Count('books')
# )

# print(books_by_category)

# for obj in books_by_category:
#     print(f"Категории: {obj['name_category']}, кол-во книг = {obj['books_count']}")
#

### **Задача 2: Диапазон цен и общее количество страниц**
# **ТЗ:** Найти минимальную, максимальную цену книг и общее количество страниц всех книг

from library.models import Book, Category, Borrow
from django.db.models import (
    Avg,
    Count,
    Min,
    Max,
    Sum,
    Case,
    When,
    Value,
    CharField,
    Subquery,
    OuterRef,
    F
)

from typing import Any

#data = Book.objects.aggregate(min_price=Min("price"), max_price=Max("price"), total_pages=Sum("page_count")

### **Задача 3: Количество книг по каждому жанру**
# **ТЗ:** Подсчитать количество книг в каждом жанре, отсортировать по убыванию количества

#count_book_by_ganre = Book.objects.values("name_category").annotate(book_count=Count("id"))

# data = Book.objects.values('category').annotate(
#     total_book=Count('id'),
# ).order_by('-total_book')
#
# for book in data:
#     print(book)

### **Задача 4: Средняя цена книг по каждому издательству**
# **ТЗ:** Вычислить среднюю цену книг для каждого издательства и количество книг у каждого издательства


# data = Book.objects.values('publisher__name').annotate(
#     avg_price=Avg("price"),
#     books_count=Count("id")
# ).order_by("books_count")
#
# for book in data:
#     print(book)

### **Задача 6: Топ-5 читателей по количеству активных займов**
# **ТЗ:** Найти 5 пользователей с наибольшим количеством невозвращенных книг


#1
# data = Borrow.objects.values('member__username').annotate(
#     count_aktiv_borrow=Count(
#         'id', filter=Q(returned=False))).order_by('-count_aktiv_borrow')[:5]  # 0 -4 index
# print(data)
#
# for el in data:
#     print(el)

#2

# data = (
#     User.objects
#     .values('last_name', 'first_name')
#     .annotate(
#         borrows_count=Count(
#             'borrows',
#             filter=Q(borrows__returned=False)
#         )
#     )
#     .order_by('-borrows_count')
# )[:5]
#
# print(data)
#
# for el in data:
#     print(el)

#3
# data = (
#     User.objects
#     .values('last_name', 'first_name')
#     .annotate(
#         borrows_count=Count(
#             'borrows',
#             filter=Q(borrows__returned=False)
#         )
#     )
#     .order_by('-borrows_count')
# )[:5]

# for el in data:
#     print(el)

### **Задача 8: Книги с количеством займов и статусом популярности**
# **ТЗ:** Для каждой книги подсчитать количество займов и пометить как популярную (>3 займов) или обычную

# data = (
#     Book.objects
#     .annotate(
#         borrow_cnt=Count("borrows"),
#         populate_status=Case(
#             When(condition=Q(borrow_cnt__gt=3), then=Value("Popular")),
#             default=Value("Ordenary"),
#             output_field=CharField())
#     ).order_by("-borrow_cnt")
# )
#
# for d in data[:10]:
#     print(f"{d.title=} --- {d.populate_status=} --- {d.borrow_cnt=}")

### **Задача 10: Книги дороже средней цены в своем жанре**
# **ТЗ:** Найти книги, цена которых превышает среднюю цену книг в том же жанре

# avg_price_subquery = (
#     Book.objects
#     .filter(category=OuterRef("category"))
# ).values("category").annotate(avg_price=Avg("price")).values("avg_price")
#
# data = (
#     Book.objects
#     .annotate(
#         avg_price_genre=Subquery(avg_price_subquery)
#     )
#     .filter(price__gt=F("avg_price_genre"))
# )
#
#
# for d in data:
#     print(f"{d.title=} --- {d.category=}:")
#     print(f"{d.price=} --- {d.avg_price_genre=}")


#тоже задание, но если речь идет про конкретные категории(жанры)

avg_price_subquery = (
    Book.objects
    .filter(category=OuterRef("category"))
).values("category").annotate(avg_price=Avg("price")).values("avg_price")

data = (
    Book.objects
    .annotate(avg_price_genre=Subquery(avg_price_subquery))
    .filter(
        category__in=[1,2], #vybor categorii
        price__gt=F('avg_price_genre'))
)


for d in data:
    print(f"{d.title=} --- {d.category=}:")
    print(f"{d.price=} --- {d.avg_price_genre=}")





