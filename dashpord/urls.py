
from django.urls import path
from .views import *

urlpatterns = [
    path("all_grade/", All_Group_staude.as_view(), name="All_Group_staude"),
    path("system_grade/<int:id>/", All_System_in_grade.as_view(), name="All_System_in_grade"),
    path("books_System/<int:id>/", Books_System.as_view(), name="Books_System"),
    path("display_book/<int:book_id>/", BookFileView.as_view(), name="BookFileView"),
    path("create_order_book/", Create_Order_Book.as_view(), name="Create_Order_Book"),
    path("book_fileView/", BookFileView.as_view(), name="BookFileView")
]