from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Authors, Quotes
from exception import has_data, has_request_data, has_value


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PATCH,DELETE')
        return response

    @app.route('/authors', methods=['GET'])
    def get_authors():
        authors = has_data(list(map(Authors.format, Authors.query.all())))
        
        return jsonify({
            'success': True,
            'authors': authors
        })
    
    @app.route('/quotes', methods=['GET'])
    def get_quotes(): 
        quotes = has_data(list(map(Quotes.format, Quotes.query.all())))
        
        return jsonify({
            'success': True,
            'quotes': quotes
        })

    @app.route('/authors/<int:author_id>/quotes', methods=['GET'])
    def get_author_quotes(author_id):
        author = has_data(Authors.query.get(author_id))
        quotes = has_data(author.quotes)
        format_quotes = [quote.format() for quote in quotes]
        
        return jsonify({
            'success': True,
            'quotes': format_quotes
        })
    
    @app.route('/authors/search', methods=['GET'])
    def search_authors():
        body = has_request_data(request.get_json())
        searchTerm = body.get('searchTerm',None)
        has_value([searchTerm])
        authors = has_data(Authors.query.filter(Authors.name.like('%'+searchTerm+'%')).all())
        format_authors = [author.format() for author in authors]

        return jsonify({
            'success':True,
            'authors': format_authors
        })
    
    @app.route('/quotes/search', methods=['GET'])
    def search_quotes():
        body = has_request_data(request.get_json())
        searchTerm = body.get('searchTerm',None)
        has_value([searchTerm])
        quotes = has_data(Quotes.query.filter(Quotes.quote.like('%'+searchTerm+'%')).all())
        format_quotes = [quote.format() for quote in quotes]

        return jsonify({
            'success':True,
            'quotes': format_quotes
        })

    @app.route('/authors', methods=['POST'])
    def add_author():
        body = has_request_data(request.get_json())
        new_name = body.get('name', None)
        new_mail = body.get('mail', None)
        has_value([new_name,new_mail])    
                           
        author = Authors(name=new_name, mail=new_mail)    
        author.insert()
            
        return jsonify({
        'success': True,
        'id': author.id
        })
            
    
    @app.route('/quotes', methods=['POST'])
    def add_quotes():
        body = has_request_data(request.get_json())
        new_quote = body.get('quote',None)
        author_id = int(body.get('author_id',0))
        author = has_value([new_quote,author_id])
        
        has_data(Authors.query.get(author_id))
        quote = Quotes(quote=new_quote,author_id=author_id)
        quote.insert()

        return jsonify({
            'success':True,
            'id':quote.id,
        })

    @app.route('/quotes/<int:quote_id>',methods=['PATCH'])
    def update_quote(quote_id):
        has_value([quote_id])
        body = has_request_data(request.get_json())
        updated_quote = body.get('quote',None)
        author_id = int(body.get('author_id', 0))
        has_value([update_quote,author_id])

        quote = has_data(Quotes.query.get(quote_id))
        if quote.author_id == author_id:
            quote.quote = updated_quote
            quote.update()

            return jsonify({
                'success':True,
                'id': quote_id
            })
        else:
            return jsonify({
                'success':False,
                'msg':'The author id was not found'
            })

    @app.route('/quotes/<quote_id>', methods=['DELETE'])
    def delete_quote(quote_id):
        has_value([quote_id])
        body = has_request_data(request.get_json())
        author_id = body.get('author_id', None)
        has_value([update_quote, author_id])

        quote = has_data(Quotes.query.get(quote_id))
        if quote.author_id == author_id:
            quote.delete()

            return jsonify({
                'success':True,
                'id': quote_id
            })
        else:
            return jsonify({
                'success':False,
                'msg':'The author id doesn\'t math'
            })
    
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success':False,
            'error':404,
            'message':'Resource not found'
        }),404      

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success':False,
            'error':404,
            'message': 'Bad Request'
        }), 400
        
    return app
