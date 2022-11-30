# smartmeter

1. Set up smartmeter data reading and storage
	- adjust root_config file to local settings
	- run ./src/create-db.py 
	- make ./read-meter.sh executable with `sudo chmod +x read-meter.sh`
	- run `crontab-e` 
	- add executing read-meter.sh to crontab with desired frequency, and adjust root to local settings, eg:
	
	 `*/5 * * * * root="/home/beerm/projects/utilities" && bash ${root}/read-meter.sh -r $root >> ${root}/logs/cron.log 2>&1`
	
	- run `sudo systemctl restart cron`
2. api & frontend as service
	- make start-server.sh and start-frontend.sh executable with `sudo chmod +x start-server.sh`
	- cp smartmeter-server.service and smartmeter-frontend.serice to /etc/systemd/system (remove _disable)
	- run `sudo systemctl enable smartmeter-server.service`
	- run `sudo systemctl start smartmeter-server.service`
	- run `sudo systemctl enable smartmeter-frontend.service`
	- run `sudo systemctl start smartmeter-frontend.service`
	- reboot
	- check status with `sudo systemctl status smartmeter-server.service` 
