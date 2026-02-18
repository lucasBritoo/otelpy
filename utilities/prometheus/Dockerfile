FROM prom/prometheus:v2.47.0

USER root
RUN chgrp -R 0 /prometheus && \
    chmod -R g+rwX /prometheus

ADD prometheus.yml /etc/prometheus

# Health Check -> http://localhost:<port>/-/healthy

CMD ["--web.listen-address=:9090", \
    "--config.file=/etc/prometheus/prometheus.yml", \
    "--web.route-prefix=/prometheus/", \
    "--web.external-url=/prometheus/", \
    "--storage.tsdb.path=/data/prometheus", \
    "--storage.tsdb.retention.time=15d"]
