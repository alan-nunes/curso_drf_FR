from .views import TodoListAndCreate, TodoDetailChangesAndDelete
# ou from . import views


from django.urls import path

urlpatterns = [
    path('todo/', TodoListAndCreate.as_view()),
    #ou path('todo/', views.todo_list, name='todo_list')
    path('todo/<int:pk>', TodoDetailChangesAndDelete.as_view()),
]