from todos.models import users,todos

session={}

def signin_required(fun):
    def wrapper(*args,**kwargs):
        if "user" in session:
            return fun(*args,**kwargs)
        else:
            print("u must login")
    return wrapper

def authenticate(**kwargs):
    username=kwargs.get("username")
    password=kwargs.get("password")
    user = [user for user in users if user["username"] == username and user["password"] == password]
    return user

class SignInView:
    def post(self,*args,**kwargs):
        username=kwargs.get("username")
        password = kwargs.get("password")
        user=authenticate(username=username,password=password)
        if user:
            session["user"]=user[0]
            print("success")

        else:
            print("invalid")

class TodoView():
    @signin_required
    def get(self, *args, **kwargs):
        return todos

    @signin_required
    def post(self, *args, **kwargs):
        userId = session["user"]["id"]
        kwargs["userId"] = userId
        todos.append(kwargs)
        print(todos)

class TodoListView:
    @signin_required
    def get(self, *args, **kwargs):
        print(session)
        userId = session["user"]["id"]
        print(userId)
        my_todo=[todo for todo in todos if todo["userId"]==userId]
        return my_todo

class TodoDetailsView:
    def get_object(self,id):
        todo=[todo for todo in todos if todo["todoId"]==id]
        return todo

    @signin_required
    def get(self, *args, **kwargs):
        todo_id = kwargs.get("todo_id")
        todo = self.get_object(todo_id)
        return todo

    @signin_required
    def delete(self, *args, **kwargs):
        todo_id = kwargs.get("todo_id")
        data = self.get_object(todo_id)
        if data:
            todo= data[0]
            todos.remove(todo)
            print("todo removed")
            print(len(todos))

    @signin_required
    def put(self, *args, **kwargs):
        todo_id = kwargs.get("todo_id")
        data = kwargs.get("data")
        instance = self.get_object(todo_id)
        if instance:
            todo_obj = instance[0]
            todo_obj.update(data)
            return todo_obj


sig=SignInView()
sig.post(username="vinu",password="Password@123")
# mytodo=TodoView()
# print(mytodo.get())
# mytodo.post(todoId=8,task_name='WiFi recharge',completed='True')
# todolist=TodoListView()
# print(mytodo.get())
todo_detail=TodoDetailsView()
todo_detail.delete(todo_id=7)
print(todo_detail.get(todo_id=3))
todo_detail=TodoDetailsView()
data={"task_name":"project submission","completed":"not completed"}
print((todo_detail.put(todo_id=6,data=data)))
