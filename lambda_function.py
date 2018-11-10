from game_servers import query_servers
import json, logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def lambda_handler(event, context):
  logger.info('Event: {}\ncontext: {}'.format(str(event), str(context)))
  return {
    'statusCode': 200,
    'body': json.dumps(query_servers(r'\appid\202090'))
  }
