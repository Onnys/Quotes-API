import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy 
from app import create_app
from models import setup_db, Quotes , Authors 


class QuotesTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'quotes_test'
        self.database_path = 'postgres://{}:{}@{}/{}'.format('onnys','onnys','localhost:5432',self.database_name)

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
    
    def tearDown(self):
        pass

    def test_404_get_quotes(self):
        Quotes.query.delete()
        response = self.client().get('/quotes')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        
    def test_get_quotes(self):
        author = Authors(name='Ricardo Lopes', mail='ricardolopes@gmail.com')
        author.insert()
        quote = Quotes(quote='Tambem nao sei', author_id=author.id)
        quote.insert()

        response = self.client().get('/quotes')
        data = json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
    
    def test_404_get_authors(self):
        Quotes.query.delete()
        Authors.query.delete()
        
        response = self.client().get('/authors')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'],False)
    
    def test_get_authors(self):
        author = Authors(name='Ricardo Lopes', mail='ricardolopes@gmail.com')
        author.insert()
        response = self.client().get('/authors')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'],True)
    
    def test_get_authors_quotes(self):
        author = Authors(name='Hernani da silva', mail='hernani@gmail.com')
        author.insert()
        quote = Quotes(quote='quanto decideres estarei aqui', author_id=author.id)
        quote.insert()

        response = self.client().get('/authors/'+str(author.id)+'/quotes')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'],True)

        
    def test_404_get_authors_quotes(self):
        Quotes.query.delete()
        Authors.query.delete()

        response = self.client().get('/authors/1/quotes')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'],False)

    def test_404_search_authors(self):
        response = self.client().get('/authors/search', json={'searchTerm':'!!!!!!!!'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code,404)
        self.assertEqual(data['success'],False)

    def test_search_authors(self):
        author = Authors(name='Artur', mail='artur@gmail.com')
        author.insert()
        response = self.client().get('/authors/search', json={'searchTerm':'Artur'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_search_quotes(self):
        Quotes.query.delete()

        response = self.client().get('/quotes/search', json={'searchTerm':'```````'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'],False)

    def test_search_quotes(self):
        author = Authors(name='Hernani da silva', mail='hernani@gmail.com')
        author.insert()
        quote = Quotes(quote='quanto decideres estarei aqui', author_id=author.id)
        quote.insert()

        response = self.client().get('quotes/search',json={'searchTerm':'aqui'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)

    def test_400_add_authors(self):
        response = self.client().post('/authors', json={'name':'DRP'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'],False)

    def test_add_authors(self):
        response = self.client().post('/authors', json={'name':'Laylizzy','mail':'Laylizzy@gmail.com'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'],True)
    
    def test_400_add_quotes(self):
        response = self.client().post('/quotes', json={'quote':'No author quote'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'],False)
 
    def test_add_quotes(self):
        response = self.client().post('/quotes', json={'quote':'1 quote','author_id':1})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'],True)

    def test_400_update_quote(self):
        author = Authors(name='Neyo', mail='neyo@gmail.com')
        author.insert()
        quote = Quotes(quote='quanto decideres estarei aqui', author_id=author.id)
        quote.insert()
        
        response = self.client().patch('/quotes/'+str(quote.id)+'', json={'quote': 'today or never'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'],False)

    def test_404_update_quotes(self):
        response = self.client().patch('/quotes/1000', json={'quote':'sera que ela nota','author_id':1})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'],False)
    
    def test_update_quote(self):
        author = Authors(name='Eusebio', mail='eusebio@gmail.com')
        author.insert()
        quote = Quotes(quote='descansa em paz papucho', author_id=author.id)
        quote.insert()
        
        response = self.client().patch('/quotes/'+str(quote.id)+'', json={'quote': 'today or never','author_id':author.id})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'],True)
    

    def test_404_delete_quote(self):
        author = Authors(name='Eusebio', mail='eusebio@gmail.com')
        author.insert()
        response = self.client().delete('/quotes/10000000', json={'author_id':author.id})
        data = json.loads(response.data)

        self.assertEqual(response.status_code,404)
        self.assertEqual(data['success'],False)
        
    def test_delete_quote(self):
        author = Authors(name='Eusebio', mail='eusebio@gmail.com')
        author.insert()
        quote = Quotes(quote='descansa em paz papucho', author_id=author.id)
        quote.insert()
        response = self.client().delete('/quotes/'+str(quote.id)+'', json={'author_id':author.id})
        data = json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
    
if __name__ == '__main__':
    unittest.main()
