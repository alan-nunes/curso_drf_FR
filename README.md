## Criando ambiente de desenvolvimento
```
python3 -m venv venv
``` 
- Verificar se ele foi criado 
    ```
    ls
    ```

- Ativar ambiente
    ```
    venv/Sctipts/activate
    ```

 ## Instalar o Django Rest Framework
    
```
    pip install djangorestframework
```

## Criar projeto
```
    django-admin startproject api_todo
```

- Verificar se o projeto foi iniciado
    
    ```
        ls
    ```

## Iniciar a 1° aplicação
Entrar na pasta do projeto criado
    
```
cd api_todo
```

Criar a primeira aplicacação
```
python manage.py startapp app
```

## Instalar APPs
No arquivo do projeto, em settings.py, em ```INSTALLED_APPS``` incluir a lib do restframework e a aplicação criada.

```
    #apps
    'app',

    #libs
    'rest_framework',
```

## Criar o 1° modelo
Na pasta api_todo/app abra o ```arquivo models.py``` e add o código a seguir

```
from django.db import models

class Todo(models.Model):
    name = models.CharField(max_length=120)
    done = models.BooleanField(default=False)
    create_at = models.DateField(auto_now_add=True) #add automaticamente a data
```
     
- É necessário após criar o modelo, ou alterações executar a migrations

     ```
     python manage.py makemigrations
     ```

- Enviar as alterções para o banco de dados
     
     ```
     python manage.py migrate
     ```

## Criar objeto
Abra o shell django:
    
```
python manage.py shell
```

 Importe o modelo ```Todo``` 
```
from app.models import Todo
```

Crie um objeto Todo
```
todo = Todo(name="Estudar Django", done=False)
todo.save()  # Salva o objeto no banco de dados.
```

Verificar se o objeto foi criado corretamente
```
todos = Todo.objects.all() # Retorna todos os objetos Todo do banco.
    for t in todos:
        print(t.name. t.done, t.create_at)
```

## Criar Serializers

Na pasta do ```app``` crie o arquivo ```serializers.py``` e adicione o seguinte código:

```
from app.models import Todo
from rest_framework import serializers

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'name', 'done', 'created_at']
```

Com isso foi criada uma classe serializadora do modelo Todo. Agora vamos abrir o terminal do projeto:

```
python manage.py shell
```

Vamos importar o modelo e a classe recém criada

```
from app.models import Todo
from app.serializers import TodoSerializer
```

Vamos serializer o objeto criado

```
todo = Todo.objects.first() ## pegando o primeiro objeto criado
```

Vamos criar uma variável para armazenar esse objeto
```
serializer = TodoSerializer(todo)
```

Para ver o objeto basta apenas:
```
serializer.data
```

## Requisições e Respostas com as Views
As views são funções ou classes que quando acessamos determinadas urls ela é chamada. As views envia e recebe dados. 
No arquivo ```views.py``` adicione o seguinte código:

```
from app.models import Todo
from app.serializers import TodoSerializer

# determina quais metodos podem serem acessados pela view (GET, POST...)
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def todo_list(request):
    todo = Todo.objects.all()  #setando uma variavel que pega todos os objetos do banco de dados e vai colocar nessa variável
    serializer = TodoSerializer(todo, many=True)    
    return Response(serializer.data)
```

Fizemos uma função que pode chamar o método GET. Agora devemos regitrar uma URL, para quando essa URL for chamada, chamar essa função. Na pasta ```app``` vamos criar um arquivo ```urls.py``` e dentro do arquivo iremos add o seguinte código:

``` 
from .views import todo_list

from django.urls import path

urlpatterns = [
    path('todo/', todo_list)
]
```

após fazer isso, abra a pasta ```api_todo```, e abra o arquivo ```urls.py``` e vamos incluir a url da aplicação, devemos atualizar os códigos para que fique da seguinte forma:

```
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]
```

Feito isso, iremos inicializar nosso servidor para realizar os testes:

```
python manage.py runserver
```

Caso não apareça mensagem de erro, é sinal que está tudo ok. Acessaremos a url http://127.0.0.1:8000/, e logo após iremos acessar http://127.0.0.1:8000/todo/ e deve ser mostrada na nossa requisição GET.

Iremos agora implementar a nossa requisição POST, para isso iremos alterar o código do arquivo ```views.py``` apenas no método ```@api_view```

```
@api_view(['GET', 'POST'])
def todo_list(request):
    if request.method == 'GET':
        todo = Todo.Objects.all()
        serializer = TodoSerializer(todo, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

Feito isso, iremos importat a classe Status
```
from rest_framework import status
```

Iremos reinicializar o servidor e verificar se deu certo. Logo após iremos criar um novo objeto:

```
{
    "name": "fazer suco"
}
```

Após esse processo iremos realizar as requisções Delete e a de detalhar o objeto. Em nosso arquivo views.py iremos incluir uma nova função.

```
@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail_change_and_delete(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)  #pega o objeto no banco de dados que contenha essa chave primária
    except Todo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = TodoSerializer(todo)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = TodoSerializer(todo, data=request.data)
            if serializer.is_valid()
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            todo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
```

Feito isso, iremos criar uma URL para essa função. no arquivo ```app\urls.py``` 

Iremos importar a view
```
from .views import todo_list, todo_detail_change_and_delete
```

Logo após criar a URL
```
path('todo/<int:pk>', todo_detail_change_and_delete),
```

Agora é so iniciar o servidor e acessar a seguinte URL ```http://localhost:8000/todo/id``` onde o id é o numero 1,2,3... Vai aparecer o botão DELETE e PUT.


## Implementando Class Based View
Na ```views.py``` iremos realizar algumas alterações:

- Iremos importar o pacote:
```
from rest_framework.views import APIView
```

Iremos refatorar a função ```todo_list``` para a classe criada abaixo:
 ```
class TodoListAndCreate(APIView):
    def get(self, request):
        todo = Todo.Object.all()
        serializer = TodoSerializer(todo, many=True)
        return Reponse(serializer.data)

    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)
 ```

 No arquivo ```app/urls.py``` remova a url ```todo_list``` e adicione a seguinte:

 ```
 path('todo', TodoListAndCreate.as_view()),
 ```

 #### Agora é reinicializar o servidor para verificar se tudo está funcionando normalmente

Iremos agora refatorar a função ```todo_detail_change_and_delete``` para a classe que iremos criar ```TodoDetailChangesAndDelete```

```
class TodoDetailChangesAndDelete(APIView):
    def get_object(self, pk):
        try:
            return Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise NotFound()
    
    def get(self, request, pk):
        todo = self.get_object(pk)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def put(self, request pk):
        todo = self.get_object(pk)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid()
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        todo = self.get_object(pk)
        todo.delete()
        return Response(status.status.HTTP_204_NOT_CONTENT)
```

Logo após iremos importar a seguinte classe:

```
from rest_framework.exceptions import NotFound
```

Iremos alterar a urls e importar o view conforme feito na refatoração da função anterior.

#### Agora é reinicializar o servidor para verificar se tudo está funcionando normalmente

## Trabalhando com classes genericas
No arquivo views.py iremos importar:

```
from rest_framework import generics
```

Iremos modicar a classe que estamos usando da seguinte forma:

```
class TodoListAndCreate(generics.ListCreateAPIView)
```

Com isso, a classe ja implementa os metodos get e post automaticamente. Dessa forma iremos apagar o corpo da classe e importar duas propriedes. Ao final, a classe vai ficar da seguinte forma:

```
class TodoDetailChangeAndDelete(generics.ListCreateAPIView):
    queryset = Todo.objects.all() #consulta ao banco de dados
    serializer_class = TodoSerializer
```

Iremos fazer o mesmo para a outra view:
```
class TodoDetailChangeAndDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
```

## Problemas que podem ocorrer

Caso não consiga ativar o ambiente virtual corretamente, o Python pode não está configurado corretamente no sistema.

Aqui estão alguns passos para resolver o problema:

Remover a pasta venv no PowerShell do VS Code:

```
Remove-Item -Recurse -Force venv
```
Explicação:

- **Recurse:** Remove todos os arquivos e subdiretórios dentro da pasta venv.
- **Force:** Força a remoção, mesmo de arquivos de leitura ou proteção.

Depois que o diretório for removido, você poderá recriar o ambiente virtual usando os comandos:

```
python -m venv venv
.\venv\Scripts\Activate 
```
Instale as dependências com:

```
pip install -r requirements.txt
```
Isso deve remover o ambiente virtual corretamente e permitir que você o recrie e configure sem problemas.