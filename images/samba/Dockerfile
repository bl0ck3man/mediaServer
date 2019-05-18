FROM alpine:3.9

RUN apk add --no-cache --update \
    samba-common-tools \
    samba-client \
    samba-server

EXPOSE 445/tcp

CMD ["smbd", "--foreground", "--log-stdout"]