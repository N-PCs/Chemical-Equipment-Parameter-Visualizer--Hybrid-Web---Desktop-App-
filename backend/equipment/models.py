"""
Equipment App - Database Models
Stores uploaded datasets with history management (last 5 datasets).
"""
from django.db import models
from django.utils import timezone


class Dataset(models.Model):
    """
    Model to store uploaded equipment datasets.
    Maintains history of last 5 uploads with summary statistics.
    """
    id = models.CharField(max_length=100, primary_key=True)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(default=timezone.now)
    
    # Summary statistics stored as JSON
    total_count = models.IntegerField()
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()
    type_distribution = models.JSONField()
    
    # Full dataset stored as JSON
    data = models.JSONField()
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Equipment Dataset'
        verbose_name_plural = 'Equipment Datasets'
    
    def __str__(self):
        return f"{self.filename} ({self.uploaded_at.strftime('%Y-%m-%d %H:%M')})"
    
    @classmethod
    def maintain_history_limit(cls):
        """
        Keep only the last 5 datasets, delete older ones.
        """
        datasets = cls.objects.all()
        if datasets.count() > 5:
            # Delete all except the 5 most recent
            to_delete = datasets[5:]
            for dataset in to_delete:
                dataset.delete()
