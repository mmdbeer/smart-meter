. /home/beerm/python/util-env/bin/activate
echo "Python environment activated"

cd /home/beerm/projects/utilities
echo "Current working directory: $PWD" 
python src/server.py %> server.log
