ARG version

FROM nextcloud:$version

ARG uid
ARG gid

#RUN apk --no-cache add shadow && usermod -u $uid _www-data && groupmod -g $gid _www-data && apk del shadow

RUN set -x \
	&& addgroup -g $gid -S _www-data \
	&& adduser -u $uid -D -S -G _www-data _www-data \
	&& chown _www-data:_www-data -R /var/www/html

WORKDIR /var/www/html