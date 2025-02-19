from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

# List of allowed endpoints for caching
CACHEABLE_ENDPOINTS = [
    "states/", "states/<int:pk>/", "departments/", "organisations/", "schemes/", 
    "schemes/<int:pk>/", "schemes/scholarship/", "schemes/job/", "criteria/", 
    "procedures/", "documents/", "scheme-documents/", "sponsors/", "scheme-sponsors/", 
    "choices/gender/", "choices/state/", "choices/category/",
    "states/<int:state_id>/departments/", "departments/<int:department_id>/schemes/", 
    "schemes/<int:scheme_id>/beneficiaries/", "schemes/<int:scheme_id>/criteria/", 
    "schemes/<int:scheme_id>/procedures/", "schemes/<int:scheme_id>/documents/", 
    "schemes/<int:scheme_id>/sponsors/", "states/<int:state_id>/schemes/", 
    "schemes/by-states/", "schemes/by-state-and-department/", 
    "schemes/multi-state-departments/"
]

class CacheMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Only cache GET requests
        if request.method != "GET":
            return None
        
        # Check if the request path is in the cacheable endpoints
        if not any(request.path.startswith(f"/api/{endpoint}") for endpoint in CACHEABLE_ENDPOINTS):
            return None
        
        cache_key = f"cache_{request.path}"
        response = cache.get(cache_key)
        if response:
            return response

    def process_response(self, request, response):
        # Only cache GET responses with 200 OK status
        if request.method == "GET" and response.status_code == 200:
            if any(request.path.startswith(f"/api/{endpoint}") for endpoint in CACHEABLE_ENDPOINTS):
                cache_key = f"cache_{request.path}"
                cache.set(cache_key, response, timeout=60 * 15)  # Cache for 15 minutes

        # Invalidate cache on data modification
        if request.method in ["POST", "PUT", "DELETE"]:
            self.invalidate_related_cache()

        return response

    def invalidate_related_cache(self):
        """Clears cache for all cacheable endpoints when data changes."""
        for endpoint in CACHEABLE_ENDPOINTS:
            cache.delete_pattern(f"cache_/api/{endpoint}*")  # Clears all related cache keys
