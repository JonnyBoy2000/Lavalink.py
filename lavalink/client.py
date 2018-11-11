import asyncio
import aiohttp
import logging
import random
from urllib.parse import quote
from .node import Node
from .nodemanager import NodeManager
from .playermanager import PlayerManager

log = logging.getLogger(__name__)


class Client:
    def __init__(self, user_id: int, shard_count: int = 1, pool_size: int = 100, loop=None):
        self._user_id = str(user_id)
        self._shard_count = str(shard_count)
        self._loop = loop or asyncio.get_event_loop()
        self.node_manager = NodeManager(self)
        self.players = PlayerManager(self)

        self._session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=pool_size, loop=loop)
        )  # This session will be used for websocket and http requests

    def add_node(self, host: str, port: int, password: str, region: str):
        """
        Adds a node to Lavalink's node manager
        ----------
        :param host:
            The address of the Lavalink node
        :param port:
            The port to use for websocket and REST connections
        :param password:
            The password used for authentication
        :param region:
            The region to assign this node to
        """
        self.node_manager.add_node(host, port, password, region)

    async def get_tracks(self, query: str, node: Node = None):
        """
        Gets all tracks associated with the given query
        -----------------
        :param query:
            The query to perform a search for
        :param node:
            The node to use for track lookup. Leave this blank to use a random node.
        """
        node = node or random.choice(self.node_manager.nodes)
        destination = 'http://{}:{}/loadtracks?identifier={}'.format(node.host, node.port, quote(query))
        headers = {
            'Authorization': node.password
        }

        async with self._session.get(destination, headers=headers) as res:
            if res == 200:
                return await res.json()

            return []

    async def voice_update_handler(self, data):
        """
        This function intercepts websocket data from your Discord library and
        forwards the relevant information on to Lavalink, which is used to
        establish a websocket connection and send audio packets to Discord.

        Example usage for Discord.py:
        -------------
        bot.add_listener(lavalink_client, 'on_socket_response')
        -------------
        :param data:
            The payload received from Discord.
        """
        if not data or 't' not in data:
            return

        if data['t'] == 'VOICE_SERVER_UPDATE':
            guild_id = int(data['d']['guild_id'])

            player = self.players.get(guild_id)

            if player:
                player._voice_server_update(data['d'])
        elif data['t'] == 'VOICE_STATE_UPDATE':
            if int(data['d']['user_id']) != int(self._user_id):
                return

            player = self.players.get(guild_id)

            if player:
                player._voice_state_update(data['d'])
        else:
            return