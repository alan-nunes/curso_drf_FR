# Django Rest Framework - Guia de Estudo

Este documento foi criado para facilitar seus estudos sobre Django Rest Framework (DRF), servindo como um guia para configurar, desenvolver e testar APIs com Django e DRF.

## Criando o Ambiente de Desenvolvimento

1. Crie um ambiente virtual para isolar as dependências do projeto:
    ```
    python3 -m venv venv
    ``` 

2. Verifique se o ambiente foi criado:
    ```
        ls
    ```

3. Ative o ambiente virtual:
    - No Windows:
    ```
    venv/Sctipts/activate
    ```

    - No Linux/Mac::
    ```
    source venv/bin/activate
    ```

 ## Instalar o Django Rest Framework
No ambiente ativado, instale o Django e o Django Rest Framework:
```
    pip install djangorestframework
```

## Criar Projeto
1. Crie o projeto principal do Django:
    ```
    django-admin startproject api_todo
    ```

2. Verifique se o projeto foi criado com sucesso:
    ```
    ls
    ```
3. Acesse a pasta do projeto:
    ```
     cd api_todo
    ```

## Criar a Primeira Aplicação
1. Crie a primeira aplicação Django dentro do projeto:
    ```
    python manage.py startapp app
    ```

## Registrar Aplicações no Django
1. No arquivo ```settings.py```, registre sua aplicação e o Django Rest Framework na lista de aplicativos instalados (```INSTALLED_APPS```):
    ```
    INSTALLED_APPS = [
        # Aplicações do projeto
        'app',

        # Bibliotecas
        'rest_framework',
    ]
    ```

## Criar o Primeiro Modelo
1. No arquivo ```models.py``` da aplicação app, crie o seguinte modelo:

    ```
    from django.db import models

    class Todo(models.Model):
        name = models.CharField(max_length=120)
        done = models.BooleanField(default=False)
        created_at = models.DateField(auto_now_add=True) #add automaticamente a data
    ```
- **name:** Um campo de texto com no máximo 120 caracteres.
- **done:** Um campo booleano para marcar se a tarefa foi concluída.
- **created_at:** Data de criação, adicionada automaticamente.
     
2. Após criar ou modificar o modelo, é necessário gerar e aplicar as migrações:
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

## Criar um Objeto no Shell Django
1. Abra o shell interativo do Django: 
    ```
    python manage.py shell
    ```

2. Importe o modelo ```Todo``` e crie um objeto:
    ```
    from app.models import Todo
    
    todo = Todo(name="Estudar Django", done=False)
    todo.save()  # Salva o objeto no banco de dados.
    ```

3. Verifique se o objeto foi criado corretamente:
    ```
    todos = Todo.objects.all() # Retorna todos os objetos Todo do banco.
    for t in todos:
        print(t.name. t.done, t.created_at)
    ```

## Criar Serializers
1. Crie um arquivo ```serializers.py``` dentro da aplicação ```app``` e adicione o seguinte código:

    ```
    from app.models import Todo
    from rest_framework import serializers

    class TodoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Todo
            fields = ['id', 'name', 'done', 'created_at']
    ```

2. O TodoSerializer é responsável por converter os dados do modelo Todo em formatos como JSON.



## Criar Views para Requisições e Respostas (GET e POST)
As views são funções ou classes que controlam a lógica de negócios da aplicação. Quando uma URL específica é acessada, uma view correspondente é chamada. Em uma API, as views enviam e recebem dados, processando requisições como ```GET```, ```POST```, ```PUT``` e ```DELETE```.

1. No arquivo ```views.py```, adicione a seguinte função para lidar com requisições ```GET``` e listar todos os itens:
    ```
    from rest_framework.decorators import api_view
    from rest_framework.response import Response
    from app.models import Todo
    from app.serializers import TodoSerializer

    @api_view(['GET'])
    def todo_list(request):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
    ```
Essa view responde com uma lista de todos os objetos da tabela Todo, convertendo-os em JSON usando o ```TodoSerializer```.

2. Agora, registre essa view em app/urls.py:
    ``` 
    from .views import todo_list
    from django.urls import path

    urlpatterns = [
        path('todo/', todo_list),
    ]
    ```

3. No arquivo principal de URLs ```(api_todo/urls.py)```, adicione as URLs da aplicação ```app```:
    ```
    from django.contrib import admin
    from django.urls import include, path

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('app.urls')),
    ]
    ```

4. Para testar, inicie o servidor:
    ```
    python manage.py runserver
    ```

Acesse a URL http://127.0.0.1:8000/todo/ e você verá a resposta da requisição ````GET```, listando todos os itens da tabela ```Todo```.

5. Agora, vamos permitir que nossa API aceite requisições ```POST```, para criar novos itens. Modifique a função ```todo_list``` no arquivo ```views.py```:
    ```
    from rest_framework import status

    @api_view(['GET', 'POST'])
    def todo_list(request):
    """
    Lida com requisições GET e POST para listar e criar itens Todo.
    """
        if request.method == 'GET':
            todos = Todo.objects.all()
            serializer = TodoSerializer(todos, many=True)
            return Response(serializer.data)
    
        elif request.method == 'POST':
            serializer = TodoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    ```

6. Agora você pode enviar requisições POST para http://127.0.0.1:8000/todo/ com o seguinte JSON, por exemplo:
    ```
    {
        "name": "fazer suco"
    }
    ```

## Criar Views para Requisições e Respostas (GET, PUT E DELETE)
1. Para permitir edição, deleção e visualização detalhada de um item Todo, adicione uma nova função no arquivo views.py:

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

2. No arquivo ```app/urls.py```, adicione a rota para essa view:
    ```
    from .views import todo_list, todo_detail_change_and_delete

    path('todo/<int:pk>', todo_detail_change_and_delete),
    ```

3. Agora, você pode acessar detalhes, editar ou deletar itens acessando ```http://localhost:8000/todo/<id>```.


## Implementando Class Based Views
Para usar Class Based Views (CBVs) no Django REST Framework, precisamos realizar algumas alterações no arquivo views.py.

1. Adicione a seguinte importação ao seu arquivo ```views.py```:
    ```
    from rest_framework.views import APIView
    ```

2. Refatore a função ```todo_list``` para uma class-based view, conforme o código abaixo:
    ```
    class TodoListAndCreate(APIView):
        def get(self, request):
            todo = Todo.object.all()
            serializer = TodoSerializer(todo, many=True)
            return Reponse(serializer.data)

        def post(self, request):
            serializer = TodoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)
    ```

 3. No arquivo ```app/urls.py``` remova a url anterior de```todo_list``` e adicione a seguinte linha:
    ```
        path('todo', TodoListAndCreate.as_view()),
    ```

4. Reinicie o servidor para verificar se tudo está funcionando corretamente:
    ```
    python manage.py runserver
    ```


5. Iremos agora refatorar a função ```todo_detail_change_and_delete```. Crie a classe ```TodoDetailChangesAndDelete`` para gerenciar as operações de detalhamento, atualização e exclusão:
    ```
    from rest_framework.exceptions import NotFound
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

6. Atualizando as URLs Novamente. No arquivo app/urls.py, adicione a URL correspondente:
    ```
    path('todo/<int:pk>/', TodoDetailChangesAndDelete.as_view()),
    ```

7. Reinicie o servidor novamente para verificar as novas implementações.

## Trabalhando com Classes Genéricas
Agora, vamos simplificar ainda mais usando classes genéricas.

1. Adicione a seguinte importação no seu views.py:
    ```
    from rest_framework import generics
    ```

2. Refatore as classes da seguinte forma para que implemente os métodos automáticamente:
    ```
    class TodoListAndCreate(generics.ListCreateAPIView)
        queryset = Todo.objects.all()  # Consulta ao banco de dados
        serializer_class = TodoSerializer
  
    class TodoDetailChangeAndDelete(generics.ListCreateAPIView):
        queryset = Todo.objects.all() #consulta ao banco de dados
        serializer_class = TodoSerializer
    ```

3. Reinicie o servidor novamente para verificar as novas implementações. Note que os métodos estão funcionando normalmente.

## Criando o ViewSet
1. Reduza as classes para apenas uma, utilizando um ViewSet. No arquivo ```views.py``` importe o pacote das viewssets:
    ```
    from rest_framework imports viewset
    ```

2.Crie a classe abaixo, e apague as demais:
    ```
    class TodoViewSet(viewset.ModelViewSet):
        queryset = Todo.objects.all()
        serializer_class = TodoSerializer
    ```

3. No arquivo app/urls.py, substitua o código existente pelo seguinte:
    ```
    from app.views import TodoViewSet
    from rest_framework.routers import DefaultRouter

    router = DefaultRouter()
    router.register(r'', TodoViewSet)

    urlpatterns = router.urls
    ```

4. Ative o ambiente de desenvolvimento e execute o servidor novamente:
    ```
    python manage.py runserver
    ```


## Problemas que Podem Ocorrer

Caso tenha dificuldades para ativar o ambiente virtual, pode ser que o Python não esteja configurado corretamente no seu sistema. Siga os passos abaixo para resolver:

1. Remover a pasta do ambiente virtual. Execute o seguinte comando no PowerShell do VS Code:
    ```
    Remove-Item -Recurse -Force venv
    ```

Explicação:

- **Recurse:** Remove todos os arquivos e subdiretórios dentro da pasta venv.
- **Force:** Força a remoção, mesmo de arquivos de leitura ou proteção.

2. Depois que o diretório for removido, você poderá recriar o ambiente virtual usando os comandos:
    ```
    python -m venv venv
    .\venv\Scripts\Activate 
    ```

3. Instalar as dependências com:
    ```
    pip install -r requirements.txt
    ```
Esses passos devem resolver problemas relacionados à configuração do ambiente virtual.

Créditos: [YouTuber Fernando Rodrigues](https://youtu.be/uly58gcUGv8?si=MhEVI_xTuBqBLUvZ) pela excelente tutoria.