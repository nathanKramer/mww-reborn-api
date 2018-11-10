import os
from flask import Flask

from game_servers import query_servers
import json, logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/v1/servers')
def server_list():
  return json.dumps(query_servers(r'\appid\202090'))

if __name__ == '__main__':
  # Bind to PORT if defined, otherwise default to 5000.
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
