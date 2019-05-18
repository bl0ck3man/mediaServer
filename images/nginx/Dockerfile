ARG version
ARG uid
ARG gid

FROM nginx:$version

RUN apk --no-cache add shadow && usermod -u $uid www-data && groupmod -g $gid www-data && apk del shadow

WORKDIR /var/www