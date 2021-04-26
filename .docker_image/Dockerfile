ARG ROOT_CONTAINER=pyiron/continuum:2021-04-13
ARG BASE_CONTAINER=$ROOT_CONTAINER
FROM $BASE_CONTAINER

LABEL maintainer="Muhammad Hassani<hassani@mpie.de>"
USER $DOCKER_UID
RUN rm -r ${HOME}/*
USER root
RUN fix-permissions /home/$DOCKER_USER && \
    fix-permissions $CONDA_DIR
# Switch back to pyiron to avoid accidental container runs as root
USER $DOCKER_UID

WORKDIR $HOME
