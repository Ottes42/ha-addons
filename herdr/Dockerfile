ARG BUILD_FROM=ghcr.io/hassio-addons/debian-base:9.5.0
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

# Persistent home: herdr state, Claude Code (binary, login, sessions),
# git config and shell history all live in /data and survive updates.
ENV \
    LANG=C.UTF-8 \
    HOME=/data/home

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG BUILD_ARCH=amd64
ARG HERDR_VERSION="0.9.3"
# hadolint ignore=DL3008
RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        git \
        jq \
        less \
        nano \
        openssh-server \
        procps \
        python3 \
        ripgrep \
        ttyd \
    \
    && if [[ "${BUILD_ARCH}" = "aarch64" ]]; then ARCH="aarch64"; fi \
    && if [[ "${BUILD_ARCH}" = "amd64" ]]; then ARCH="x86_64"; fi \
    && curl -fsSL -o /usr/local/bin/herdr \
        "https://github.com/herdrdev/herdr/releases/download/v${HERDR_VERSION}/herdr-linux-${ARCH}" \
    && chmod +x /usr/local/bin/herdr \
    \
    && usermod -d /data/home root \
    && rm -f /etc/ssh/ssh_host_* \
    && rm -rf /var/lib/apt/lists/*

COPY rootfs /

RUN chmod +x /etc/s6-overlay/s6-rc.d/*/run
