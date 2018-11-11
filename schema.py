import graphene

from game_servers import query_servers, get_players_for_ip

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeneralInformation(graphene.ObjectType):
    client_download_url = graphene.String()
    client_version = graphene.String()
    discord_invite = graphene.String(
        default_value='https://discord.gg/gAbfpTZ')


class PlayerInGame(graphene.ObjectType):
    name = graphene.String()
    score = graphene.String()
    duration = graphene.Float()


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
    players = graphene.List(
        PlayerInGame, description='Players currently in game')

    def resolve_steam_link(self, info):
        return 'steam://{}'.format(self.ipaddress)

    def resolve_players(self, info):
        logger.info(
            "[Server name={}]. Resolving players.\n{}".format(self.name, info))

        players = []
        if self.player_count > 0:  # Don't query steam redundantly.
            def player(player_values):
                logger.info(player_values)
                name = player_values['name'] or '[Name Hidden]'
                return PlayerInGame(name=name, duration=player_values['duration'], score=player_values['score'])
            players = list(map(player, get_players_for_ip(self.ipaddress)))
        return players


class Match(graphene.ObjectType):
    time = graphene.Time()
    id = graphene.ID()
    game_mode = graphene.String()
    level = graphene.String()
    player_count = graphene.Int()
    players = graphene.List(Player)
    status = graphene.String()


class Query(graphene.ObjectType, description="The MWW Reborn API's root GraphQL schema"):
    servers = graphene.List(
        Server, description='The list of currently online servers')
    players = graphene.List(Player, description='The players')
    matches = graphene.List(Match, description="MWW Match history")
    general_information = graphene.Field(
        GeneralInformation, description='General information about the MWW Reborn project', default_value=GeneralInformation())

    def resolve_servers(self, info):
        server_list = []
        logger.info("Resolving servers.\n{}".format(info))
        for server in query_servers(r'\appid\202090'):
            server_list.append(Server(
                name=server['name'], player_count=server['players'], ipaddress=server['server_addr']))

        return server_list


schema = graphene.Schema(query=Query)
