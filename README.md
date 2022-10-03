# smartmeter

1. automatic data gathering: run reading.py in crontab
	- make read-meter.sh executable with sudo chmod +x read-meter.sh
	- crontab-e 
	- add: """ */5 * * * * bash /home/beerm/Documents/python/smartmeter/read-meter.sh >> /home/beerm/Documents/python/smartmeter/cron.log 2>&1 """ 
	- sudo systemctl restart cron
2. api & frontend as service
	- make start-server.sh and start-frontend.sh executable with sudo chmod +x start-server.sh
	- cp smartmeter-server.service and smartmeter-frontend.serice to /etc/systemd/system (remove _disable)
	- sudo systemctl enable(and start) smartmeter-server(and frontend).service
	- reboot
	- check status with sudo systemctl status smartmeter-server.service 
