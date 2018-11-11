from steam import game_servers as gs

def get_players_for_ip(ipaddress):
    addr = ipaddress.split(':')
    addr = tuple([addr[0], int(addr[1])])
    return gs.a2s_players(addr)

def query_servers(query, max_servers=10):
    servers = []
    for server_addr in gs.query_master(query, max_servers=max_servers):
        info = gs.a2s_info(server_addr)
        info['server_addr'] = ':'.join(map(str, server_addr))
        servers.append(info)

    return servers
