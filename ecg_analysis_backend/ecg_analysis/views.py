from django.http import HttpResponse
from ecg_analysis.fileprocessor.fileprocessor import FileProcessor


def index(request):
    file = request.FILES['files']
    proc = FileProcessor()
    proc.process(file)
    return HttpResponse("hello.")
