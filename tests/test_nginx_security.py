from pathlib import Path


CONFIG_PATH = Path(__file__).parents[1] / "deploy" / "nginx" / "mypalai.space.conf"


def _config() -> str:
    return CONFIG_PATH.read_text(encoding="utf-8")


def test_https_server_defines_security_headers() -> None:
    config = _config()

    assert "listen 443 ssl" in config
    assert 'Strict-Transport-Security "max-age=31536000" always' in config
    assert 'X-Content-Type-Options "nosniff" always' in config
    assert 'X-Frame-Options "DENY" always' in config
    assert 'Referrer-Policy "strict-origin-when-cross-origin" always' in config
    assert 'Permissions-Policy "camera=(), microphone=(), geolocation=()" always' in config
    assert "Content-Security-Policy" in config
    assert "default-src 'self'" in config
    assert "frame-ancestors 'none'" in config


def test_hsts_is_not_sent_by_plain_http_server() -> None:
    config = _config()
    http_server, https_server = config.split("# HTTPS server", maxsplit=1)

    assert "Strict-Transport-Security" not in http_server
    assert "Strict-Transport-Security" in https_server


def test_http_redirects_to_canonical_https_host() -> None:
    config = _config()

    assert "return 301 https://mypalai.space$request_uri;" in config
