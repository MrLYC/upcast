"""Representative Django pagination patterns for offset scanning tests."""

from django.core.paginator import Paginator as PageList
from django.db import connection
from django.db.models.expressions import RawSQL
from rest_framework.pagination import CursorPagination, LimitOffsetPagination, PageNumberPagination

from app.models import User


users = User.objects.order_by("id")
page = request.GET.get("page")
page_size = 50
offset = (page - 1) * page_size

window = users[offset : offset + page_size]
zero_offset = users[0:page_size]
open_ended = users[offset:]
limit_only = users[:page_size]
ordinary = [1, 2, 3, 4][1:3]

paginator = PageList(users, page_size)
page_object = paginator.get_page(request.GET.get("page"))


class UserPagePagination(PageNumberPagination):
    page_size = 100


class UserOffsetPagination(LimitOffsetPagination):
    default_limit = 20


class UserCursorPagination(CursorPagination):
    page_size = 100


class UserListView:
    pagination_class = LimitOffsetPagination


raw_queryset = User.objects.raw("SELECT * FROM users LIMIT %s OFFSET %s", [page_size, offset])
raw_expression = RawSQL("id IN (SELECT id FROM users LIMIT 50 OFFSET 100)", [])

with connection.cursor() as cursor:
    cursor.execute(f"SELECT * FROM users LIMIT {page_size} OFFSET {offset}")
