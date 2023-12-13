import pprint, requests, json

IMAGE = 'https://imgbed.sanyue.site/api/v1'
UPLOAD = '/upload'

def upload(file):
    r = requests.post(IMAGE+UPLOAD, )
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_view(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        data = json.loads(request.POST.get('data'))
        username = data['username']
        response_data = {
            'status': True,
            'message': 'File uploaded successfully',
            'data': {
                'key': 'unique_key',
                'name': uploaded_file.name,
                'size': uploaded_file.size,
                # 其他文件信息
            },
            'links': {
                'url': IMAGE + UPLOAD + uploaded_file.name,
                # 其他链接信息
            }
        }
        return JsonResponse(response_data)
    return JsonResponse({'status': False, 'message': 'Invalid request method'})