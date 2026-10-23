ARG BUILD_FROM=ghcr.io/hassio-addons/debian-base:9.5.0
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

# Persistent home: herdr state, Claude Code (binary, login, sessions),
# git config and shell history all live in /data and survive updates.
# Global npm packages go to ~/.local as well (bin in ~/.local/bin), caches to
# ~/.cache; both are excluded from backups (backup_exclude in config.yaml).
ENV \
    LANG=C.UTF-8 \
    HOME=/data/home \
    NPM_CONFIG_PREFIX=/data/home/.local \
    NPM_CONFIG_CACHE=/data/home/.cache/npm \
    NPM_CONFIG_UPDATE_NOTIFIER=false

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG BUILD_ARCH=amd64
ARG HERDR_VERSION="0.9.3"
ARG TTYD_VERSION="1.7.7"
ARG HA_CLI_VERSION="5.5.0"
ARG YQ_VERSION="4.54.1"
ARG NODE_VERSION="24.22.0"
ARG GH_VERSION="2.102.0"
ARG UV_VERSION="0.13.1"
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
        python3-websockets \
        python3-yaml \
        ripgrep \
        vim \
        xz-utils \
    \
    && if [[ "${BUILD_ARCH}" = "aarch64" ]]; then ARCH="aarch64"; fi \
    && if [[ "${BUILD_ARCH}" = "amd64" ]]; then ARCH="x86_64"; fi \
    && curl -fsSL -o /usr/local/bin/herdr \
        "https://github.com/herdrdev/herdr/releases/download/v${HERDR_VERSION}/herdr-linux-${ARCH}" \
    && curl -fsSL -o /usr/local/bin/ttyd \
        "https://github.com/tsl0922/ttyd/releases/download/${TTYD_VERSION}/ttyd.${ARCH}" \
    && if [[ "${BUILD_ARCH}" = "aarch64" ]]; then GOARCH="arm64"; fi \
    && if [[ "${BUILD_ARCH}" = "amd64" ]]; then GOARCH="amd64"; fi \
    && curl -fsSL -o /usr/local/bin/ha \
        "https://github.com/home-assistant/cli/releases/download/${HA_CLI_VERSION}/ha_${BUILD_ARCH}" \
    && curl -fsSL -o /usr/local/bin/yq \
        "https://github.com/mikefarah/yq/releases/download/v${YQ_VERSION}/yq_linux_${GOARCH}" \
    && chmod +x /usr/local/bin/herdr /usr/local/bin/ttyd /usr/local/bin/ha /usr/local/bin/yq \
    \
    && if [[ "${BUILD_ARCH}" = "aarch64" ]]; then NODEARCH="arm64"; fi \
    && if [[ "${BUILD_ARCH}" = "amd64" ]]; then NODEARCH="x64"; fi \
    && curl -fsSL "https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-${NODEARCH}.tar.xz" \
        | tar -xJ -C /usr/local --strip-components=1 \
            "node-v${NODE_VERSION}-linux-${NODEARCH}/bin" "node-v${NODE_VERSION}-linux-${NODEARCH}/lib" \
    && node --version && npm --version \
    && curl -fsSL "https://github.com/cli/cli/releases/download/v${GH_VERSION}/gh_${GH_VERSION}_linux_${GOARCH}.tar.gz" \
        | tar -xz -C /usr/local/bin --strip-components=2 "gh_${GH_VERSION}_linux_${GOARCH}/bin/gh" \
    && curl -fsSL "https://github.com/astral-sh/uv/releases/download/${UV_VERSION}/uv-${ARCH}-unknown-linux-gnu.tar.gz" \
        | tar -xz -C /usr/local/bin --strip-components=1 \
            "uv-${ARCH}-unknown-linux-gnu/uv" "uv-${ARCH}-unknown-linux-gnu/uvx" \
    && gh --version && uv --version \
    \
    && sed -i 's#^\(root:[^:]*:0:0:[^:]*:\)/root:#\1/data/home:#' /etc/passwd \
    && grep -q '^root:.*:/data/home:' /etc/passwd \
    && rm -f /etc/ssh/ssh_host_* \
    && rm -rf /var/lib/apt/lists/*

COPY rootfs /

RUN chmod +x /etc/s6-overlay/s6-rc.d/*/run /usr/local/bin/herdr-env \
        /usr/local/bin/ha-* /usr/local/bin/esphome-* /usr/local/bin/herdr-agents \
        /usr/local/bin/herdr-extensions /usr/local/lib/herdr/ttyd-index \
        /usr/local/bin/osc52-copy \
    && for name in xclip xsel wl-copy wl-paste; do \
        ln -s osc52-copy "/usr/local/bin/$name"; \
    done

LABEL \
    org.opencontainers.image.title="Home Assistant App: herdr" \
    org.opencontainers.image.description="Dauerhaft laufender herdr-Server für Coding-Agents (Claude Code)" \
    org.opencontainers.image.source="https://github.com/Ottes42/ha-addons"
