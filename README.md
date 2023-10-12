# slider-daemon
Slider Daemon

A Daemon that uses SLIDER-cli to download the latest full disk of a satellite of your choice and set it as your background
This is a `Client <> Server` application as SLIDER-cli is written in Go

On server:
Open daemon.json and change any settings, any ports you change must be mirrored in the client config
Run sliderDaemon.py

On client:
Open daemon.json and change any settings to match your server (ip and ports)
Start sliderClient.py and observe logs

