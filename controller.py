#!/usr/bin/env python3
from client import Client, Spell, Input
from base64 import b64decode
from cmd import Cmd

PLAYERID = 11
SECRET = b64decode(b"NIUs3BwkJbuleutDs44d051NfN8KVmJgJ5+wxLGUEok=")
# SERVER = "192.168.1.2"
SERVER = "127.0.0.1"
PORT = 2004

spellmap = {
    "fireball": Spell.Fireball,
    "infernoorbs": Spell.InfernoOrbs,
    "flamewall": Spell.FlameWall,
    "lightningspike": Spell.LightningSpike,
    "sparknova": Spell.SparkNova,
    "electrotrap": Spell.Electrotrap,
    "icewave": Spell.IceWave,
    "frostaura": Spell.FrostAura,
    "freezingrain": Spell.FreezingRain,
        }

inputmap = {
    "up": Input.UP,
    "down": Input.DOWN,
    "left": Input.LEFT,
    "right": Input.RIGHT,
    "a": Input.A,
    "b": Input.B,
    "lt": Input.LT,
    "rt": Input.RT,
    "start": Input.START,
    "select": Input.SELECT,
        }


class Controller(Cmd):
    intro = """Welcome to the neversaydie remote control."""
    prompt = "> "

    def preloop(self):
        print(f"Connecting to {SERVER} on port {PORT} as player {PLAYERID}.")
        self.client = Client(PLAYERID, SECRET, SERVER, PORT)

    def do_cast(self, spell):
        """Cast a spell
  Options are:
   fireball
   infernoorbs
   flamewall
   lightningspike
   sparknova
   electrotrap
   icewave
   frostaura
   freezingrain
        """
        if spell not in spellmap:
            print(f"{spell} isn't a valid spell. Pleast try again.")
            return
        op = spellmap[spell]
        self.client.cast(op)

    def do_input(self, input_op):
        """Send an button input
  Options are:
   up
   down
   left
   right
   a
   b
   lt
   rt
   start
   select
        """
        if input_op not in inputmap:
            print(f"{input_op} isn't a valid input. Pleast try again.")
            return
        op = inputmap[input_op]
        self.client.input(op)

    def do_text(self, data):
        """Send text data."""
        self.client.text(data.encode())

    def do_rawcmd(self, cmdop):
        """Send a raw command int and opcode int"""
        vals = cmdop.split(" ")
        if len(vals != 2):
            print(f"Must send only 2 integers as input. The cmd and the opcode.")
            return

        cmd, op = vals
        cmd, op = int(cmd), int(op)
        self.client.command(cmd, op)


if __name__ == "__main__":
    Controller().cmdloop()
