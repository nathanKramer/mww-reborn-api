import graphene

from game_servers import query_servers

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Player(graphene.ObjectType):
    name = graphene.String()
    match_count = graphene.Int()
    win_count = graphene.Int()
    loss_count = graphene.Int()
    rating = graphene.Float()
    wins = graphene.List('schema.Match')
    losses = graphene.List('schema.Match')
    matches = graphene.List('schema.Match')

class Server(graphene.ObjectType):
    name = graphene.String()
    player_count = graphene.Int()
    ipaddress = graphene.String()
    steam_link = graphene.String()
    players = graphene.List(Player)

    def resolve_steam_link(self, info):
        return 'steam://{}'.format(self.ipaddress)

class Match(graphene.ObjectType):
    time = graphene.Time()
    id = graphene.ID()
    game_mode = graphene.String()
    level = graphene.String()
    player_count = graphene.Int()
    players = graphene.List(Player)
    status = graphene.String()

class Query(graphene.ObjectType):
    servers = graphene.List(Server)
    players = graphene.List(Player)
    matches = graphene.List(Match)

    def resolve_servers(self, info):
        server_list = []
        logger.info("Resolving servers.")
        for server in query_servers(r'\appid\202090'):
            server_list.append(Server(
                name=server['name'], players=server['players'], ipaddress=server['server_addr']))

        return server_list


schema = graphene.Schema(query=Query)
