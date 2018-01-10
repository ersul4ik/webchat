FROM debian:stretch

ENV USERID 1000
ENV GROUPID 1000

RUN apt-get update \
    && apt-get install -y --no-install-recommends certbot \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -g $GROUPID app \
    && useradd -r -u $USERID -g $GROUPID app \
    && mkdir -p /var/lib/letsencrypt && mkdir -p /etc/letsencrypt && mkdir -p /var/log/letsencrypt \
    && chown -R $USERID:$GROUPID /etc/letsencrypt /var/lib/letsencrypt /var/log/letsencrypt

ADD entrypoint.sh /

USER app

VOLUME /etc/letsencrypt /var/lib/letsencrypt

ENTRYPOINT ["/entrypoint.sh"]
