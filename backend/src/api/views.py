from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import Equipment, FileUpload
from core.services import process_csv, cleanup_old_uploads, get_summary_stats
from .serializers import EquipmentSerializer, FileUploadSerializer

from rest_framework.permissions import IsAuthenticated

class EquipmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly viewset for listing equipment.
    Can filter by upload_id.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = EquipmentSerializer
    queryset = Equipment.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        upload_id = self.request.query_params.get('upload_id')
        if upload_id:
            queryset = queryset.filter(file_upload_id=upload_id)
        return queryset

class FileUploadViewSet(viewsets.ModelViewSet):
    """
    Handles file uploads.
    """
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Process the file
        instance = serializer.instance
        try:
            count = process_csv(instance)
            cleanup_old_uploads()
            headers = self.get_success_headers(serializer.data)
            return Response(
                {
                    **serializer.data,
                    "message": f"Successfully processed {count} records.",
                    "count": count
                },
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Returns summary stats for the latest upload or specific upload_id
        """
        upload_id = request.query_params.get('upload_id')
        stats = get_summary_stats(upload_id)
        if stats is None:
            return Response({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)
            
        return Response(stats)

    @action(detail=True, methods=['get'])
    def report(self, request, pk=None):
        """
        Generates and returns a PDF report.
        """
        from django.http import FileResponse
        from core.services import generate_report
        
        buffer = generate_report(pk)
        if buffer is None:
             return Response({"error": "Report generation failed or file not found"}, status=status.HTTP_404_NOT_FOUND)
             
        return FileResponse(buffer, as_attachment=True, filename=f'report_{pk}.pdf')
