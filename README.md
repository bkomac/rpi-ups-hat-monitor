# rpi-ups-hat
Python script to stop InfluxDB and shotdow RPI on battery low level

## Start script as a service
```bash
cd /lib/systemd/system
sudo vi ups.service
```


```bash
sudo chmod 644 /lib/systemd/system/ups.service
chmod +x /home/pi/python/rpi-ups-hat/ups-monitor.py
sudo systemctl daemon-reload
sudo systemctl enable ups.service
sudo systemctl start ups.service
```
