from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import SharedContent, UploadedFile
import json

def get_shared_content():
    content, created = SharedContent.objects.get_or_create(id=1)
    return content

def index(request):
    shared = get_shared_content()
    files = UploadedFile.objects.all().order_by('-uploaded_at')
    return render(request, 'chor/index.html', {
        'content': shared.content,
        'files': files
    })

def sync(request):
    shared = get_shared_content()
    if request.method == 'POST':
        data = json.loads(request.body)
        shared.content = data.get('content', '')
        shared.save()
        return JsonResponse({'status': 'success'})
    
    files = list(UploadedFile.objects.all().order_by('-uploaded_at').values('id', 'filename', 'content'))
    return JsonResponse({
        'content': shared.content,
        'files': files
    })

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        try:
            # Try to read content for display if it's text
            content_str = ""
            try:
                # We need to read a copy to not exhaust the stream for the FileField
                content_str = uploaded_file.read().decode('utf-8')
                uploaded_file.seek(0) # Reset pointer
            except:
                content_str = "[Binary File - No preview available]"

            custom_title = request.POST.get('title')
            filename = custom_title if custom_title else uploaded_file.name

            new_file = UploadedFile.objects.create(
                file=uploaded_file,
                filename=filename,
                content=content_str
            )
            total_count = UploadedFile.objects.count()
            return JsonResponse({
                'status': 'success', 
                'id': new_file.id, 
                'filename': new_file.filename,
                'total': total_count
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=400)

def download_file(request, file_id):
    file_obj = get_object_or_404(UploadedFile, id=file_id)
    if file_obj.file:
        response = HttpResponse(file_obj.file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_obj.filename}"'
        return response
    else:
        # Fallback for old records without physical file
        response = HttpResponse(file_obj.content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{file_obj.filename}"'
        return response

def update_file(request, file_id):
    if request.method == 'POST':
        file_obj = get_object_or_404(UploadedFile, id=file_id)
        data = json.loads(request.body)
        file_obj.content = data.get('content', '')
        file_obj.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
