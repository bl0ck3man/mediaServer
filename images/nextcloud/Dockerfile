ARG uid
ARG gid
ARG version

FROM nextcloud:$version

RUN set -x \
	&& addgroup -g $gid -S _www-data \
	&& adduser -u $uid -D -S -G _www-data _www-data \
	&& chown _www-data:_www-data -R /var/www/html

WORKDIR /var/www/html