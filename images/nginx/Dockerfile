ARG version

FROM nginx:1.16.0-alpine

ARG uid
ARG gid

RUN apk --no-cache add shadow
RUN echo $uid && usermod -u $uid www-data
RUN groupmod -g $gid www-data && apk del shadow

WORKDIR /var/www