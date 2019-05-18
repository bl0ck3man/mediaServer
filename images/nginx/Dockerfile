ARG version
ARG uid
ARG gid

FROM nginx:1.16.0-alpine

RUN apk --no-cache add shadow
RUN usermod -u $uid www-data
RUN groupmod -g $gid www-data && apk del shadow

WORKDIR /var/www