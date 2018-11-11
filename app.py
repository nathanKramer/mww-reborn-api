import os
import logging
from flask import Flask, json
from flask_graphql import GraphQLView

from schema import schema
from game_servers import query_servers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

env = os.getenv('ENVIRONMENT', 'development')
is_dev = env == 'development'

# Most of the hard work will be done with graphql.
app.add_url_rule(
    '/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=is_dev, pretty=is_dev))

# More explicit REST resources here, as we need them.
@app.route('/v1/servers')
def server_list():
    response = json.jsonify(query_servers(r'\appid\202090'))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
