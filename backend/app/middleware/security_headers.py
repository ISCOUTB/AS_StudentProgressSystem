from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Agrega cabeceras de seguridad HTTP a todas las respuestas."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # Previene MIME sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        # Bloquea que la app se muestre en iframes (clickjacking)
        response.headers["X-Frame-Options"] = "DENY"
        # Protección básica contra XSS en navegadores antiguos
        response.headers["X-XSS-Protection"] = "1; mode=block"
        # Fuerza HTTPS por 1 año incluyendo subdominios
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        # Controla la información del Referer enviada en peticiones
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        # Desactiva acceso a geolocalización, micrófono y cámara
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        # Política de seguridad de contenido
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https://fastapi.tiangolo.com;"
        )
        return response
