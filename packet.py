#!/usr/bin/env python3
from enum import IntEnum
from struct import pack, unpack
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hmac


def sign(data, secret_key):
    h = hmac.new(secret_key, data, "sha256")
    hmacSignature = h.digest()[:32]
    return hmacSignature


class Op(IntEnum):
    Input = 1
    Magic = 2
    Text = 3


class RequestPacket:

    def __init__(self,
                 opcode: int,
                 player_id: int,
                 data: int | bytes):
        self.opcode = opcode
        self.player_id = player_id
        self.data = data

    def encrypted_data(self, secret_key: bytes) -> bytes:
        assert type(self.data) is bytes

        cipher = AES.new(secret_key, AES.MODE_CBC, iv=b"\x00" * 16)
        padded_data = pad(self.data, block_size=16)
        ct = cipher.encrypt(padded_data)
        return ct

    def serialize(self, secret_key: bytes) -> bytes:
        enc_data = b""
        data_field = self.data

        if type(self.data) is bytes:
            enc_data = self.encrypted_data(secret_key)
            data_field = len(enc_data)
            packed_data = pack("<BBH", self.opcode, self.player_id, data_field)
        else:
            packed_data = pack("<BBHHH", self.opcode, self.player_id, data_field, 3, 0)
            packed_data += enc_data
            packed_data += sign(packed_data, secret_key)

        return packed_data


class ResponsePacket:
    packet_type_str = "Generic"

    def __init__(self, data: bytes, signature=True):
        self.signature = data[-32:] if signature else None
        self.data = data[:-32] if signature else data
        self.packet_type = self.data[0]
        self.packet_id = unpack("<H", self.data[1:3])

    def check_signature(self, secret_key):
        if self.signature is None:
            return False

        return sign(self.data, secret_key) == self.signature


class LocationPacket(ResponsePacket):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.map_id = unpack("<H", self.data[3:5])
        self.health1 = unpack("<H", self.data[5:7])
        self.health2 = unpack("<H", self.data[7:9])
