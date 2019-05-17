ARG version

FROM mysql:$version

ARG uid
ARG gid

RUN usermod -u $uid mysql && \
    groupmod -g $gid mysql