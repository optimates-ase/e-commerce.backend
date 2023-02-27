from flask import Flask, request
from flask_graphql import GraphQLView

from api.services.welcome import init_db

from api.schema.eet_v1 import schema

from flask_cors import CORS


def init_api():

    api = Flask(__name__)
    api.debug = True

    # add default query for GraphQL concept exploration
    default_query = '''
    {
        allEmployees {
            edges {
                node {
                    id,
                    firstname,
                    lastname,
                    department {
                        id,
                        name
                    },
                    role {
                        id,
                        name
                    }
                }
            }
        }
    }
    '''.strip()

    api.add_url_rule(
        "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
    )

    @api.route('/')
    def hello_world():
        return {'message': 'Hello, world!'}, 200

    @api.route('/')
    def import_data():
        request_data = request.get_json()
        return request_data, 200

    init_db()
    api.run()
