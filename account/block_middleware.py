# from django.http import JsonResponse
# import json
# class BlockMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#                 # Exclude admin page from middleware
#         if request.path.startswith('/course/') or request.path.startswith('/user/') or request.path.startswith('/teacher/') or request.path.startswith('/banner/') or request.path.startswith('/get/users/') or request.path.startswith('/live/'):
#             return response
#         if request.user.is_authenticated:
#             if 'application/json' in response.get('Content-Type', ''):
#                 if request.user.is_student:
#                     response_data = json.loads(response.content)
#                     # print("resp",response_data,response,response.content)
#                     response_data['is_blocked'] = request.user.is_block
#                     response = JsonResponse(response_data)
#         return response
from django.http import JsonResponse
import json
class BlockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # if request.user.is_authenticated and request.user.is_block:
        #     response_data={}
        #     response_data['is_blocked'] = request.user.is_block

        #     return JsonResponse(response_data, status=403)

        response = self.get_response(request)

        if request.user.is_authenticated and 'application/json' in response.get('Content-Type', ''):
            try:
                if request.user.is_block:
                    response_data = json.loads(response.content)
                    if isinstance(response_data, dict):
                        response_data.clear()  # Remove any existing data
                        response_data['is_blocked'] = request.user.is_block
                        response = JsonResponse(response_data, status=403)
                    else:
                        return response
            except ValueError:
                pass

        return response


