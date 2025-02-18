from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

class CacheMiddleware(MiddlewareMixin):
    def process_request(self, request):
        cache_key = f"cache_key_{request.path}"
        response = cache.get(cache_key)
        if response:
            return response

    def process_response(self, request, response):
        cache_key = f"cache_key_{request.path}"
        cache.set(cache_key, response, timeout=60 * 15)  # Cache for 15 minutes
        return response

        