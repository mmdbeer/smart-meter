. /home/beerm/Documents/python/sm-env/bin/activate
echo "Python environment activated"

cd /home/beerm/Documents/projects/utilities
echo "Current working directory: $PWD"
streamlit run src/frontend/frontend.py --server.headless=true
