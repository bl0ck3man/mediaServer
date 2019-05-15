FROM mysql:8.0.16

ARG uid
ARG gid

RUN usermod -u $uid  mysql && \
    groupmod -g $gid mysql