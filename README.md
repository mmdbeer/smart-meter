# smartmeter

1. Set up smartmeter data reading and storage
	- adjust root_config to local settings
	- run ./src/create-db.py 
	- make ./read-meter.sh executable with sudo chmod +x read-meter.sh
	- crontab-e 
	- add executing read-meter.sh to crontab with desired frequency, and adjust root to local settings, eg:
	
	 ''' */5 * * * * root="/home/beerm/projects/utilities" && bash \${root}/read-meter.sh -r $root >> ${root}/logs/cron.log 2>&1 ''' 
	
	- sudo systemctl restart cron
2. api & frontend as service
	- make start-server.sh and start-frontend.sh executable with sudo chmod +x start-server.sh
	- cp smartmeter-server.service and smartmeter-frontend.serice to /etc/systemd/system (remove _disable)
	- sudo systemctl enable(and start) smartmeter-server(and frontend).service
	- reboot
	- check status with sudo systemctl status smartmeter-server.service 
