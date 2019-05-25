FROM stanback:alpine-samba

ARG uid
ARG gid

RUN addgroup -g $gid -S smbgrp \
	&& adduser -u $uid -D -S -G smbgrp smbgrp \

#EXPOSE 445/tcp

#CMD ["smbd", "--foreground", "--log-stdout"]