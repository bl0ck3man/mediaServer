FROM alpine:edge

ARG uid
ARG gid

RUN apk add --update \
    samba-common-tools \
    samba-client \
    samba-server \
    && rm -rf /var/cache/apk/*

RUN addgroup -g $gid -S smbgrp \
	&& adduser -u $uid -D -S -G smbgrp smbgrp \

EXPOSE 445/tcp

ENTRYPOINT ["smbd", "--foreground", "--log-stdout"]
CMD []