#!/bin/bash

usage="$(basename "$0") [-r root]
Start fast-api server for dashboard requests
where:
	-r root directory of project, where file 'root_config' is located
	-h show help text"

#retrieve root dir from arguments
while getopts ':hr:' flag ; do
	case "$flag" in
		h) echo "$usage"; exit;;
		r) root="${OPTARG}";;
		?) printf "missing root dir"; echo "$usage" >&2; exit 1;;
	esac
done

if [ ! "${root}" ]; then
	echo "root dir must be provided"
	echo "${usage}" >&2; exit 1
fi

#read config file
source "${root}/root_config"

#activate python environment
source "${pyenv}/bin/activate"
echo "Python environment activated"

cd ${root}
echo "Current working directory: $PWD"
streamlit run src/frontend/frontend.py --server.headless=true
