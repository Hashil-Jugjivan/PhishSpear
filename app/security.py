from flask_talisman import Talisman

def init_talisman(app):
    csp = {
        "default-src": ["'self'"],
        "base-uri": ["'self'"],
        "object-src": ["'none'"],
        "img-src": ["'self'", "data:", "blob:"],
        "font-src": ["'self'", "data:", "https://fonts.gstatic.com", "https://cdn.jsdelivr.net"],
        "style-src": [
            "'self'",
            "'unsafe-inline'",
            "https://fonts.googleapis.com",
            "https://cdn.jsdelivr.net",
            "https://cdnjs.cloudflare.com",
            "https://unpkg.com"
        ],
        "script-src": [
            "'self'",
            # if you have small inline scripts during development use the nonce path below instead of keeping unsafe-inline
            # "'unsafe-inline'"
            "https://cdn.jsdelivr.net",
            "https://cdnjs.cloudflare.com",
            "https://unpkg.com"
        ],
        "connect-src": ["'self'"],
        "frame-ancestors": ["'none'"]
    }

    Talisman(
        app,
        content_security_policy=csp,
        # turn on nonce support for inline scripts you explicitly mark
        content_security_policy_nonce_in=["script-src"],
        strict_transport_security=True,
        strict_transport_security_max_age=31536000,
        strict_transport_security_include_subdomains=True,
        referrer_policy="strict-origin-when-cross-origin",
        session_cookie_secure=True,
        session_cookie_http_only=True,
        session_cookie_samesite="Lax"
    )

    @app.after_request
    def set_extra_headers(resp):
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
        return resp