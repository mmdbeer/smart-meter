. /home/beerm/python/util-env/bin/activate
echo "Python environment activated"

cd /home/beerm/projects/utilities
echo "Current working directory: $PWD"
streamlit run src/frontend/frontend.py --server.headless=true
