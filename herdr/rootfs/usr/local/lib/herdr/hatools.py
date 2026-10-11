"""Shared helpers for the herdr Home Assistant tools (stdlib only)."""
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

SUPERVISOR = "http://supervisor"
_S6_TOKEN = Path("/run/s6/container_environment/SUPERVISOR_TOKEN")


def token():
    value = os.environ.get("SUPERVISOR_TOKEN")
    if not value and _S6_TOKEN.is_file():
        value = _S6_TOKEN.read_text().strip()
    if not value:
        die("SUPERVISOR_TOKEN is not available")
    return value


def die(message, code=1):
    print(f"{Path(sys.argv[0]).name}: {message}", file=sys.stderr)
    sys.exit(code)


def request(method, url, body=None, headers=None, timeout=60, auth=True):
    """Send a request, with the Supervisor token unless auth is False. Returns (status, headers, bytes)."""
    data = None
    hdrs = {"Authorization": f"Bearer {token()}"} if auth else {}
    if body is not None:
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        hdrs["Content-Type"] = "application/json"
    hdrs.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.headers, resp.read()
    except urllib.error.HTTPError as err:
        return err.code, err.headers, err.read()
    except urllib.error.URLError as err:
        die(f"{method} {url} failed: {err.reason}")


def core(method, path, body=None, timeout=60):
    """Home Assistant Core REST API via the Supervisor proxy, returns parsed JSON or text."""
    status, _, raw = request(method, f"{SUPERVISOR}/core/api/{path.lstrip('/')}", body, timeout=timeout)
    return status, _decode(raw)


def supervisor(method, path, body=None, timeout=60):
    """Supervisor API, returns (status, data or message)."""
    status, _, raw = request(method, f"{SUPERVISOR}/{path.lstrip('/')}", body, timeout=timeout)
    payload = _decode(raw)
    if isinstance(payload, dict) and "result" in payload:
        return status, payload.get("data") if payload["result"] == "ok" else payload.get("message")
    return status, payload


def _decode(raw):
    text = raw.decode("utf-8", "replace")
    try:
        return json.loads(text)
    except ValueError:
        return text


def dump(value):
    if isinstance(value, str):
        print(value)
    else:
        print(json.dumps(value, indent=2, ensure_ascii=False))


def read_json_arg(arg):
    """Parse a JSON argument; '-' reads stdin."""
    if arg is None:
        return None
    text = sys.stdin.read() if arg == "-" else arg
    try:
        return json.loads(text)
    except ValueError as err:
        die(f"invalid JSON: {err}")


ESPHOME_SLUGS = ["5c53de3b_esphome", "5c53de3b_esphome-beta", "5c53de3b_esphome-dev"]
ESPHOME_SETUP_HINT = (
    "in the ESPHome add-on enable 'leave_front_door_open' and map port 6052 "
    "under Network, or set ESPHOME_URL"
)


def esphome_url():
    """Base URL of the ESPHome Device Builder on its own port."""
    if os.environ.get("ESPHOME_URL"):
        return os.environ["ESPHOME_URL"].rstrip("/")
    slugs = [os.environ["ESPHOME_ADDON"]] if os.environ.get("ESPHOME_ADDON") else ESPHOME_SLUGS
    for slug in slugs:
        status, info = supervisor("GET", f"addons/{slug}/info")
        if status != 200 or not isinstance(info, dict) or info.get("state") != "started":
            continue
        port = (info.get("network") or {}).get("6052/tcp")
        if not port:
            raise RuntimeError(f"{slug}: port 6052 is not mapped; {ESPHOME_SETUP_HINT}")
        return f"http://{info.get('ip_address') or 'homeassistant'}:{port}"
    raise RuntimeError(f"no running ESPHome add-on found ({', '.join(slugs)})")
