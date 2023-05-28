from enum import IntEnum
from pwn import remote, log
from packet import RequestPacket, Op


class Input(IntEnum):
    """TODO: Figure out the correct input values for these."""
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    A = 5
    B = 6
    LT = 7
    RT = 8
    START = 9
    SELECT = 10


class Spell(IntEnum):
    """TODO: Figure out the correct input values for these."""
    Fireball = 1
    InfernoOrbs = 2
    FlameWall = 3
    LightningSpike = 4
    SparkNova = 5
    Electrotrap = 6
    IceWave = 7
    FrostAura = 8
    FreezingRain = 9


class Client:
    def __init__(self,
                 player_id: int,
                 secret: bytes,
                 server: str = "192.168.1.2",
                 port: int = 2004):
        self.secret = secret
        self.player_id = player_id
        self.server = server
        self.port = port
        self._connect(server, port)

    def _send(self, packet: RequestPacket):
        serialized_packet = packet.serialize(self.secret)
        try:
            self.sock.send(serialized_packet)
        except EOFError:
            self._connect(self.server, self.port)
            self.sock.send(serialized_packet)

    def _connect(self, server, port):
        log.info(f"Connecting to {server}:{port}")
        if self.sock is not None:
            self.sock.close()
        self.sock = remote(server, port, typ="udp")

    def input(self, action: Input):
        log.info(f"Sending input: {action._name_}")
        packet = RequestPacket(Op.Input, self.player_id, action)
        self._send(packet)

    def cast(self, spell: Spell):
        log.info(f"Casting spell: {spell._name_}")
        packet = RequestPacket(Op.Magic, self.player_id, spell)
        self._send(packet)

    def text(self, msg: bytes):
        log.info(f"Sending text: {msg}")
        packet = RequestPacket(Op.Text, self.player_id, msg)
        self._send(packet)

    def command(self, cmd: int, op: int):
        log.info(f"Attempting command: {cmd} with operation: {op}")
        packet = RequestPacket(cmd, self.player_id, op)
        self._send(packet)
