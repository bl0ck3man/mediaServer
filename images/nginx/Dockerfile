ARG version

FROM nginx:$version

ARG uid
ARG gid

RUN apk --no-cache add shadow
RUN usermod -a -u $uid www-data -G www-data
RUN groupmod -g $gid www-data && apk del shadow

WORKDIR /var/www