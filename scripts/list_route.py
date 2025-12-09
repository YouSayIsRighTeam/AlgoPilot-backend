from app.main import app
from fastapi.routing import APIRoute

print(f"{'Method':<10} {'Path':<30} {'Name'}")
print("-" * 50)

for route in app.routes:
    if isinstance(route, APIRoute):
        methods = ", ".join(route.methods)
        print(f"{methods:<10} {route.path:<30} {route.name}")