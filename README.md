# Raw Paster

Raw Paster is a simple REST service that handle raw data to be send from a terminal
to a webserver quickly.

A better description may come... a day :D

# How to install ?

Well it's easy ! Just a quick setup and we are done !

First, clone this git :

```
cd /my/install/path && git clone https://github.com/FunkySayu/rawpaster
```

Create an alias to the client in your `.{bash,zsh}rc` :

```
alias rawpaster="python3 /my/install/path/rawpaster/client.py"
```

You're done !

# How to use ?

You send something in `stdin`, the client catch it and send it to a server. For example :

```
ps aux | grep python | rawpaster -H http://raw.funkysayu.fr -k my_key
```

You can also put your default host (`http://raw.funkysayu.fr` for example) in the `RAWPASTER_CLIENT_HOST` environment
variable. Same for the default key, in the `RAWPASTER_CLIENT_KEY`.

```
export RAWPASTER_CLIENT_HOST="http://raw.funkysayu.fr"
export RAWPASTER_CLIENT_KEY="my_key"
```

Thanks to that, the above command is only

```
ps aux | grep python | rawpaster
```

# How to get a key ?

You can create your own server and simply add a new key in the `authorized_keys.txt` file. If you want to
use my server, feel free to ask for a key !
