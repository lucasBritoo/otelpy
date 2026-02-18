FROM grafana/grafana:11.1.0

# Config Datasources
ADD datasource.yml /etc/grafana/provisioning/datasources/

ENV GF_AUTH_ANONYMOUS_ENABLED true
ENV GF_AUTH_ANONYMOUS_ORG_ROLE Admin

# ENV GF_SERVER_ROOT_URL https://test/grafana
# ENV GF_SERVER_SERVE_FROM_SUB_PATH true

# ADD grafana.ini /etc/grafana/