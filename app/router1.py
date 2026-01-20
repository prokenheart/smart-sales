def not_found(event):
    return {"statusCode": 404, "body": "Not Found"}

def service_router(event, resource, handlers):
    path = event["path"]
    method = event["httpMethod"]

    if path == f"/{resource}":
        handler = handlers["collection"].get(method)
        if handler:
            return handler(event)

    if path.startswith(f"/{resource}/"):
        handler = handlers["item"].get(method)
        if handler:
            return handler(event)

    return not_found(event)
