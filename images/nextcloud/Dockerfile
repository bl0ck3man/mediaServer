ARG version

FROM nextcloud:$version

ARG uid
ARG gid

RUN usermod -u $uid www-data && \
    groupmod -g $gid www-data

WORKDIR /var/www/html