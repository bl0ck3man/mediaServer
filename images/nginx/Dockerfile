ARG version

FROM nginx:1.16.0-alpine

ARG uid
ARG gid

RUN apk --no-cache add shadow
RUN echo $uid && usermod -u $uid www
RUN groupmod -g $gid www && apk del shadow

WORKDIR /var/www