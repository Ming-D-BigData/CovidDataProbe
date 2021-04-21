#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

set -e

MOUNT_POINT=/home/jovyan/vol_mount
[ -d ${MOUNT_POINT} ] || mkdir ${MOUNT_POINT}
SAMPLE_PROGRAM_DIR=${MOUNT_POINT}/sample_programs
SOURCE_DIR=/home/jovyan/source

[ -d ${SAMPLE_PROGRAM_DIR} ] || mkdir ${SAMPLE_PROGRAM_DIR}
chmod a+rwx ${SAMPLE_PROGRAM_DIR}
[ -f ${SAMPLE_PROGRAM_DIR}/ottawa_on_ca.ipynb ] || cp ${SOURCE_DIR}/ottawa_on_ca.ipynb ${SAMPLE_PROGRAM_DIR}/ 
[ -f ${SAMPLE_PROGRAM_DIR}/toronto_on_ca.ipynb ] || cp ${SOURCE_DIR}/toronto_on_ca.ipynb ${SAMPLE_PROGRAM_DIR}/ 

( cd /home/jovyan; FLASK_ENV=development FLASK_APP=main.py flask run --host=0.0.0.0 ) &

wrapper=""
if [[ "${RESTARTABLE}" == "yes" ]]; then
    wrapper="run-one-constantly"
fi

if [[ ! -z "${JUPYTERHUB_API_TOKEN}" ]]; then
    # launched by JupyterHub, use single-user entrypoint
    exec /usr/local/bin/start-singleuser.sh "$@"
elif [[ ! -z "${JUPYTER_ENABLE_LAB}" ]]; then
    . /usr/local/bin/start.sh $wrapper jupyter lab "$@" 
else
    echo "WARN: Jupyter Notebook deprecation notice https://github.com/jupyter/docker-stacks#jupyter-notebook-deprecation-notice."
    ( cd ${MOUNT_POINT} ; . /usr/local/bin/start.sh $wrapper jupyter notebook --NotebookApp.token='' --NotebookApp.password='' "$@" )
fi


