import asyncio
import aiohttp
import logging

from . import Node

log = logging.getLogger(__name__)


class Client:
    def __init__(self, user_id: int, shard_count: int = 1, loop=None, pool_size: int = 30):
        self._user_id = str(user_id)
        self._shard_count = str(shard_count)
        self._loop = loop or asyncio.get_event_loop()

        self._session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=pool_size, loop=loop)
        )  # This session will be used for websocket and http requests

    async def get_tracks(self, query: str, node: Node = None):
        """
        Gets all tracks associated with the given query
        -----------------
        :param node:
            The node to use for track lookup. Leave this blank to use a random node.
        :param query:
            The query to perform a search for
        """
        pass
