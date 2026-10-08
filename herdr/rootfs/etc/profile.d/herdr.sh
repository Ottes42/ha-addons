# Login shells (SSH, web terminal) get the same environment as herdr panes
export PATH="${HOME}/.local/bin:${PATH}"
if [ -r /run/s6/container_environment/SUPERVISOR_TOKEN ]; then
    SUPERVISOR_TOKEN="$(cat /run/s6/container_environment/SUPERVISOR_TOKEN)"
    export SUPERVISOR_TOKEN
fi
