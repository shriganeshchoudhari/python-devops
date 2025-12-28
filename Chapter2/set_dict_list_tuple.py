# When checking if a server exists → use a set (fast membership test)
servers = {"app1", "app2"}
print("app1" in servers)  # True

# Representing Kubernetes pod metadata → use a dict (key-value pairs)
pod_metadata = {
    "name": "web-pod",
    "namespace": "default",
    "labels": {"app": "web", "tier": "frontend"}
}

# Fixed ports (80, 443) → use a tuple (immutable sequence)
ports = (80, 443)

# API response body → use a dict (JSON-like structure)
api_response = {
    "status": "success",
    "data": {"id": 123, "message": "OK"}
}