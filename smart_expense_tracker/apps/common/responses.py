from rest_framework.response import Response


def success_response(message="Success", data=None, status_code=200):
    return Response(
        {
            "success": True,
            "message": message,
            "data": data if data is not None else {},
        },
        status=status_code,
    )
