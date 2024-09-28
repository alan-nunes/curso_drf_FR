from .views import todo_list, todo_detail_change_and_delete
# ou from . import views


from django.urls import path

urlpatterns = [
    path('todo/', todo_list),
    #ou path('todo/', views.todo_list, name='todo_list')
    path('todo/<int:pk>', todo_detail_change_and_delete),
]