FROM alpine:edge

ARG uid
ARG gid

RUN apk add --update \
    samba-common-tools \
    samba-client \
    samba-server \
    && rm -rf /var/cache/apk/*

RUN addgroup -g $gid -S samba \
	&& adduser -u $uid -D -S -G samba samba

EXPOSE 445/tcp

ENTRYPOINT ["smbd", "--foreground", "--log-stdout"]
CMD []