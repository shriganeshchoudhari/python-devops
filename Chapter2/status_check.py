servers = [
    {"name": "app1", "status": "running"},
    {"name": "app2", "status": "stopped"},
]

for server in servers:
    if server["status"] == "running":
        print(f"{server['name']} -> OK")
    else:
        print(f"{server['name']} -> NOT OK")