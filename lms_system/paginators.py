from rest_framework.pagination import PageNumberPagination


class ListPagination(PageNumberPagination):
    """Общий пагинатор для вывода списка курсов (Course) и уроков (Lesson)."""

    page_size = 3
    page_size_query_param = "user_page_size"
    max_page_size = 50
