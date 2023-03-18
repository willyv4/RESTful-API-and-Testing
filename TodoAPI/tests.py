import json
from unittest import TestCase

from app import app
from models import db, Todo


# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///todo_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()


class TestTodos(TestCase):
    """Tests for views about desserts."""

    def setUp(self):
        """Make demo data."""
        self.app = app.test_client()

        Todo.query.delete()
        db.session.commit()

        todo = Todo(title='Test Todo')
        db.session.add(todo)
        db.session.commit()

        self.todo_id = todo.id

    def tearDown(self):
        """Clean up fouled transactions."""
        db.session.rollback()

    def test_get_todo(self):
        print("######################################")
        print("Testing GET todo...")
        response = self.app.get(f'/api/todos/{self.todo_id}')
        data = json.loads(response.data)
        print(f"Response: {response}")
        print(f"Data: {data}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['todo']['id'], self.todo_id)
        self.assertEqual(data['todo']['title'], 'Test Todo')

    def test_create_todo(self):
        print("######################################")
        print("Testing CREATE todo...")
        data = {'title': 'New Todo'}
        response = self.app.post(
            '/api/todos', data=json.dumps(data), content_type='application/json')
        data = json.loads(response.data)
        print(f"Response: {response}")
        print(f"Data: {data}")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['todo']['title'], 'New Todo')

    def test_update_todo(self):
        print("######################################")
        print("Testing UPDATE todo...")
        data = {'title': 'Updated Todo', 'done': True}
        response = self.app.patch(
            f'/api/todos/{self.todo_id}', data=json.dumps(data), content_type='application/json')
        data = json.loads(response.data)
        print(f"Response: {response}")
        print(f"Data: {data}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['todo']['title'], 'Updated Todo')
        self.assertEqual(data['todo']['done'], True)

    def test_delete_todo(self):
        print("######################################")
        print("Testing DELETE todo...")
        response = self.app.delete(f'/api/todos/{self.todo_id}')
        data = json.loads(response.data)
        print(f"Response: {response}")
        print(f"Data: {data}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'DELETED')
        self.assertIsNone(Todo.query.get(self.todo_id))
