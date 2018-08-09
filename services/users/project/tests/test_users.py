# services/users/project/test_users.py


import json
import unittest


from project import db
from project.api.models import User
from project.tests.base import BaseTestCase


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """Tests for the Users Service"""

    def test_users(self):
        """Ensure the /ping route behaves correctly"""
        response = self.client.get('users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure a new user can be added to the database"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'kemal',
                    'email': 'abcd@gmail.com'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('abcd@gmail.com was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload!', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """Ensure error is thrown if the JSON object does not have
        a username key"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'abcd@gmail.com'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload!', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists"""
        with self.client:
            # add first user
            self.client.post(
                '/users',
                data=json.dumps(
                    {
                        'email': 'abcd@gmail.com',
                        'username': 'kemal'
                    }
                ),
                content_type='application/json',
            )
            # add second user
            response = self.client.post(
                '/users',
                data=json.dumps(
                    {
                        'email': 'abcd@gmail.com',
                        'username': 'kemal'
                    }
                ),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertIn('Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])
            self.assertEqual(response.status_code, 400)

    def test_single_user(self):
        """Ensure get single user behaves correctly"""
        user = add_user(username='kemal', email="abcd@gmail.com")
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('kemal', data['data']['username'])
            self.assertIn('abcd@gmail.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided"""
        with self.client:
            response = self.client.get(f'/users/absdasfder')  # this is not id
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if an id is does not exist"""
        with self.client:
            response = self.client.get(f'/users/999')  # id does not exists
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Ensure get all users behaves correctly"""
        add_user("ahmet", "ahmet@gmail.com")
        add_user("mehmet", "mehmet@gmail.com")
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('ahmet', data['data']['users'][0]['username'])
            self.assertIn('ahmet@gmail.com', data['data']['users'][0]['email'])
            self.assertIn('mehmet', data['data']['users'][1]['username'])
            self.assertIn('mehmet@gmail.com', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])


if __name__ == '__main__':
    unittest.main()
