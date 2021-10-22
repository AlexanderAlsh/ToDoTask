import flask
import werkzeug
from flask.scaffold import _endpoint_from_view_func
from werkzeug.utils import cached_property

flask.helpers._endpoint_from_view_func = _endpoint_from_view_func
werkzeug.cached_property = cached_property

"""
Столкнулся с проблемой: cannot import name 'cached_property' from 'werkzeug'
Пришлось использовать костыль сверху
В этот раз также не нашел решения проблемы
"""

from flask import Flask, request, jsonify
from flask_restplus import Api, fields, Resource
import peewee
import datetime


app = Flask(__name__)
db = peewee.SqliteDatabase('tasks_data.db')
api = Api()
api.init_app(app)


# Таблицы

class BaseModel(peewee.Model):
    class Meta:
        database = db


class Task(BaseModel):
    id = peewee.PrimaryKeyField(null=False)
    title = peewee.CharField(max_length=100)
    content = peewee.TextField(null=False)
    created_at = peewee.DateTimeField(default=datetime.datetime.now())




model = api.model('Taskmodel',
                  {'title': fields.String('Введите название'),
                   'content': fields.String('Введите описание')
                   })


# Программа

@api.route('/api/task/get/<int:id>')
class getdata(Resource):
    def get(self, id):
        task_get_id = Task.get(id)
        task_data = {}
        task_data['id'] = task_get_id.id
        task_data['title'] = task_get_id.title
        task_data['content'] = task_get_id.content
        task_data['created_at'] = task_get_id.created_at
        return jsonify(task_data)




@api.route('/api/task/post')
class postdata(Resource):
    @api.expect(model)
    def post(self):
        task_add = Task(title=request.json['title'], content=request.json['content'])
        task_add.save()
        return {'message': 'data added to database'}


@api.route('/api/task/put/<int:id>')
class putdata(Resource):
    @api.expect(model)
    def put(self, id):
        task_upd = Task.get(id)
        task_upd.title = request.json['title']
        task_upd.content = request.json['content']
        task_upd.save()
        return {'message': 'data updated'}



@api.route('/api/task/delete/<int:id>')
class deletedata(Resource):
    def delete(self, id):
        task_delete = Task.get(id)
        task_delete.delete_instance()
        task_delete.save()
        return {'message': 'data deleted successfully'}




@api.route('/api/task/get_all')
class getall(Resource):
    def get(self):
        tasks = Task.select()
        output = []
        for task in tasks:
            task_data = {}
            task_data['title'] = task.title
            task_data['content'] = task.content
            output.append(task_data)
        return jsonify(output)



if __name__ == '__main__':
    try:
        db.connect()
        Task.create_table()
    except peewee.InternalError as px:
        print(str(px))
    app.run(debug=True)
