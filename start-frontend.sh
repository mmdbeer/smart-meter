. /home/beerm/Documents/python/sm-env/bin/activate
echo "Python environment activated"

cd /home/beerm/Documents/python/smartmeter
echo "Current working directory: $PWD" 
streamlit run src/frontend/frontend.py --server.headless=true
