from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from .models import Worker



def get_all_worker_data(request, pk, model, serializer):
    if request.user.is_authenticated:
        worker = get_object_or_404(Worker, pk=pk)
        if request.user != worker.user:
            return Response(data={"detail": "Не найдено."}, status=status.HTTP_400_BAD_REQUEST)
        data = model.objects.filter(worker__user=request.user, worker__id=pk)
        serializer = serializer(data, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response(data={"error":"you are not authenticated"}, status=status.HTTP_400_BAD_REQUEST)