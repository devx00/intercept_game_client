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





if __name__ == "__main__":
    from base64 import b64decode
    secret_key = b64decode(b"NIUs3BwkJbuleutDs44d051NfN8KVmJgJ5+wxLGUEok=")
    rp = RequestPacket(3, 11, b"This is test data").serialize(secret_key)
    testdata = [
            b"A\n\xf4)\x00<\x00<\x00d\x00\xf1\x05\x02\x00\x01\x00w\x00|\x00\x03\x00NSD \x03w\x00|\x00\x03\x00NSD \x03\x01\x00 \x00\xea`\xc6P\x8cDA\xac9\xd0\xe0!(,\x05lc\xf1B\xb9L\x11\xbdt\xc9\xe9\xb1[\xee\x15\x9f\xb3sl:a\xe9\xb9\x0e\x07Z2\x8e\xcb;6\x06\xcd}e\xd4\x89\xf4S\x10\x96k\xe8\x89\x8aShY\xe4"
            b"A\x0b\xf4)\x00<\x00<\x00d\x00\xf1\x05\x02\x00\x01\x00w\x00|\x00\x03\x00NSD \x03w\x00|\x00\x03\x00NSD \x03\x00\x00\x00\x00\xb3\x06\xf6D\x0f\x9d\xbc\x83\xcb\xae\x0b&\xd37\xdc)0\xf8,\x05\x16\x8dN\xaf\x95\xb6H\x81\x1bP\x1f\xb7",
            b"A\x0c\xf4)\x00<\x00<\x00d\x00\xf1\x05\x02\x00\x01\x00w\x00|\x00\x03\x00NSD \x03w\x00|\x00\x03\x00NSD \x03\x00\x00\x00\x00\x8e\x06\xc7x\xeaYc\xd6\x85\x0e\xf3\xbbS\xef\xfe\xda\xdf\x13\xafN\x9c#\x8a\xda\xbdc\x0e_L\xf0\xbb\x0e",
            b"A\r\xf4)\x00<\x00<\x00d\x00\xf1\x05\x02\x00\x01\x00w\x00|\x00\x03\x00NSD \x03w\x00|\x00\x03\x00NSD \x03\x00\x00\x00\x00a \xe9\xba\xee\xe2\xc1jN\r\xb3U\x95\t\xe5\x9eJ\x93h\xe7\xd5\xfd\xfb\x12)\x04\x14\xabS.\r\x07",
            b"A\x0e\xf4)\x00<\x00<\x00d\x00\xf1\x05\x02\x00\x01\x00w\x00|\x00\x03\x00NSD \x03w\x00|\x00\x03\x00NSD \x03\x00\x00\x00\x00\xb75\x9b\xcb\x9f>\xedP|Y'\xe0\xc7O0\tz\xb9\xa7\x90k\xea|,3@\xd4\xb8X\x07yF",
            ]
    for l in testdata:
        signature = sign(l[:-32], secret_key)
        check = l[-32:]
        if signature == check:
            print(l[:-32])

