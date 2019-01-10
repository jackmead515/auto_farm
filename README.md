# auto_farm

## A software solution for an autonomous plant growth chamber

![alt text](https://github.com/jackmead515/auto_farm/blob/master/interface/public/images/auto_farm_dashboard.png)


### TO INSTALL

#### Get a PI
Install Raspbian on a Raspberry Pi 3B^. It's recommended to use WIFI because it's much cooler and easier.

#### Get some equipment
To have an autonomous chamber, you'll need the following sensors: <br/>
4x Soil moisture sensors -> (link) <br/>
2x Temperature and humidity sensors -> (link) <br/>
1x submersible water pump -> (link) <br/>
up to 4x web cameras for phenotyping (optional) -> (link) <br/>
1x 110V growth light -> (link) <br/>
2x Ifrared heat lamps -> (link) <br/>
1x 4 slot 5V-110V relay board -> (link) <br/>
1x MCP3008 ADC converter (optional) -> (link) <br/>
1x optical water level sensor (optional) -> (link) <br/>
1x have fun (optional) <br/>

#### Install dependencies
```

sudo apt-get update
sudo apt-get install build-essential python3-dev python3-pip python3-smbus sqlite3 git fswebcam

sudo pip3 install --upgrade distribute
sudo pip3 install ipython
sudo pip3 install --upgrade RPi.GPIO
sudo pip3 install Adafruit_DHT
sudo pip3 install adafruit-mcp3008

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
