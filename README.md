# auto_farm

## A software solution for an autonomous plant growth chamber

### TO INSTALL

#### Get a PI
Install Raspbian on a Raspberry Pi 3B^. It's recommended to use WIFI because it's much cooler and easier.

#### Get some equipment
To have an autonomous chamber, you'll need the following sensors:
4x Soil moisture sensors -> (link)
2x Temperature and humidity sensors -> (link)
1x submersible water pump -> (link)
up to 4x web cameras for phenotyping (optional) -> (link)
1x 110V growth light -> (link)
2x Ifrared heat lamps -> (link)
1x 4 slot 5V-110V relay board -> (link) 

#### Install dependencies
``` 

sudo apt-get update
sudo apt-get install python3-dev python3-pip sqlite3 git fswebcam

sudo pip3 install --upgrade distribute
sudo pip3 install ipython
sudo pip3 install --upgrade RPi.GPIO
sudo pip3 install Adafruit_DHT

curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs

```

### Clone the repository
```

cd ~
git clone https://github.com/jackmead515/auto_farm

```

### Install interface dependencies
```

cd ~/auto_farm/interface
sudo npm install --save

```

### Modify for your setup

Modify the values for the GPIO pins in **source/values.py** depending on your setup.
