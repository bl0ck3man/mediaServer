ARG version

FROM nginx:$version

ARG uid
ARG gid

RUN apk --no-cache add shadow \
   && adduser -D -u $uid -G www-data www-data \
   && groupmod -g $gid www-data \
   && apk del shadow

WORKDIR /var/www