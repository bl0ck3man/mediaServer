FROM stanback/alpine-samba:latest

ARG uid
ARG gid

RUN addgroup -g $gid -S samba \
	&& adduser -u $uid -D -S -G samba samba
