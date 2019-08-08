SDG1025 control web interface
----

This code is part of this blog post here:
[https://www.stupid-projects.com/write-python-scripts-for-your-siglent-sdg1025](https://www.stupid-projects.com/write-python-scripts-for-your-siglent-sdg1025)

This is a web interface to control a very basic functionality of the SDG1025
via a web interface. The web application is made using `flask`, `wtforms`,
`flask-socketio` and web-sockets. The back-end is running on python. I've
chosen flask, because I had to use [python-usbtmc](https://github.com/python-ivi/python-usbtmc)
API in order to be able to communicate with the SDG1025 via USB and the
USBTMC protocol.

The code was based on a template example from [here](https://github.com/miguelgrinberg/Flask-SocketIO)
which I've altered to my needs and added a custom jquery-ui interface.

You can see a video testing the web interface here:

[![IMAGE ALT TEXT](https://www.youtube.com/watch?v=T_TcUBbF5Wc/0.jpg)](https://www.youtube.com/watch?v=T_TcUBbF5Wc "Siglent SDG1025 web interface")

## Prerequisites
To use the web interface you need to install some things first:

```sh
sudo apt install python3-pip
sudo apt install libusb-1.0-0-dev

# Install python dependencies
pip3 install setuptools
pip3 install pyusb
pip3 install flask
pip3 install wtforms
pip3 install flask-socketio
pip3 install eventlet

# install python-usbtmc
git clone https://github.com/python-ivi/python-usbtmc
sudo python setup.py install
```

## Usage
To use the web interface you need to connect your host (I've used a nanopi-neo)
to the SDG1025 via a USB cable and then clone the repo and run the web app.

```sh
git clone git@bitbucket.org:dimtass/web-interface-for-sdg1025.git
cd web-interface-for-sdg1025
python3 sdg1025-web-interface.py
```

This will run the web app and now you can connect on the server IP
on port 5000, e.g.
```
http://192.168.0.65:5000
```

See more info in the blog post [here](https://www.stupid-projects.com/write-python-scripts-for-your-siglent-sdg1025)

## Author
Dimitris Tassopoulos <dimtass@gmail.com> 2019