. /home/beerm/Documents/python/sm-env/bin/activate
echo "Python environment activated"

cd /home/beerm/Documents/projects/utilities
echo "Current working directory: $PWD" 
python src/server.py %> server.log
