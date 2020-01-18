from django.http import HttpResponse
from ecg_analysis.fileprocessor.fileprocessor import FileProcessor


def index(request):
    file = request.FILES['files']
    proc = FileProcessor()
    preds = proc.process(file)
    return HttpResponse(preds)
