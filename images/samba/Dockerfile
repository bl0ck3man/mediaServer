ARG uid
ARG gid

FROM stanback:alpine-samba

RUN addgroup -g $gid -S smbgrp \
	&& adduser -u $uid -D -S -G smbgrp smbgrp \

#EXPOSE 445/tcp

#CMD ["smbd", "--foreground", "--log-stdout"]