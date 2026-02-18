FROM grafana/tempo:2.4.1

# Health check -> localhost:8023/status
COPY tempo.yaml /etc/tempo/tempo.yaml

CMD [ "--target=all", "--auth.enabled=false", "--config.file=/etc/tempo/tempo.yaml" ]
