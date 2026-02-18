FROM grafana/loki:3.0.0

USER root

ADD local-config.yaml /etc/loki/
# Health Check -> /distributor/ring

CMD [ "-config.file=/etc/loki/local-config.yaml" ]
