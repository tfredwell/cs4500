# noinspection PyProtectedMember
import asyncio
import functools

from cozmo.conn import CozmoConnection, EvtConnected
from cozmo.run import FirstAvailableConnector


class RobotConnection:
    def __init__(self):
        self.connection: CozmoConnection = None

    async def connect(self):
        connector = FirstAvailableConnector()
        loop = asyncio.get_event_loop()
        factory = functools.partial(CozmoConnection, loop=loop)

        async def conn_check(coz_conn):
            await coz_conn.wait_for(EvtConnected, timeout=5)

        async def connect():
            return await connector.connect(loop, factory, conn_check)

        transport, connection = await connect()
        self.connection = connection
        return await self.connection.wait_for_robot()

    async def disconnect(self):
        await self.connection.shutdown()
        self.connection = None

    async def is_connected(self):
        if self.connection is None:
            return False
        else:
            return self.connection.is_connected
