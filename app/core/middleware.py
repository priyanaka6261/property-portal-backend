import time
from fastapi import Request


async def logging_middleware(request: Request, call_next):
    start_time = time.time()

    # Process request
    response = await call_next(request)

    # Calculate time taken
    process_time = time.time() - start_time

    print(
        f"{request.method} {request.url} "
        f"Status: {response.status_code} "
        f"Completed in {process_time:.4f}s"
    )

    return response
