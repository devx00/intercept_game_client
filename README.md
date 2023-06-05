# The Intercept 2023 Game Client

This is a game client I wrote for [The Intercept 2023](https://www.layerone.org/events/the-intercept-hw-ctf/).
It unfortunately never fully worked but the text packets did work and they allowed us to get the goon flag by sending lowercase characters for our username.

## Interactive Commandline
There is an interactive commandline that can be started by executing `controller.py`. It offers a few commands for sending different packet types.

```sh
$ ./controller.py
Welcome to the neversaydie remote control.
> help

Documented commands (type help <topic>):
========================================
cast  help  input  rawcmd  text

>
```

To send some text (ie "myusername") you could just run:

```sh
> text myusername
```


