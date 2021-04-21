FROM jupyter/datascience-notebook:r-4.0.3

RUN pip install Flask==1.1.2 \
    && pip install Flask-Table==0.5.0 \
    && pip install markdown==3.3.4 

EXPOSE 5000
EXPOSE 8888

COPY app /home/jovyan/app
COPY source /home/jovyan/source 
COPY main.py /home/jovyan/main.py
COPY README.md /home/jovyan/README.md

USER root
RUN cd /tmp \
    && cp /usr/local/bin/start-notebook.sh . \
    && chmod 777 start-notebook.sh \
    && patch start-notebook.sh < /home/jovyan/source/start-notebook.diff \
    && cp start-notebook.sh /usr/local/bin/ \
    && rm -f start-notebook.sh \
    && mkdir /home/jovyan/vol_mount \
    && chown 1000.1000 /home/jovyan/vol_mount

VOLUME /home/jovyan/vol_mount

USER jovyan 
CMD ["start-notebook.sh"]
Entrypoint ["tini", "-g", "--"]
