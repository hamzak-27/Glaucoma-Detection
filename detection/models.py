from django.db import models
from django.utils import timezone
import uuid
import os

def get_upload_path(instance, filename):
    """Generate a unique path for uploaded fundus images."""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads/fundus_images', filename)

class Patient(models.Model):
    """Patient model to store basic information."""
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class GlaucomaTest(models.Model):
    """Model to store glaucoma test results."""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='tests')
    image = models.ImageField(upload_to=get_upload_path)
    
    # Test results
    is_glaucoma = models.BooleanField(null=True)
    confidence_score = models.FloatField(null=True)
    raw_score = models.FloatField(null=True)
    
    # Result visualization
    result_image = models.ImageField(upload_to='uploads/results', null=True, blank=True)
    
    # Metadata
    date_created = models.DateTimeField(auto_now_add=True)
    date_processed = models.DateTimeField(null=True, blank=True)
    processing_time = models.FloatField(null=True, blank=True)  # in seconds
    
    # Status tracking
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-date_created']
    
    def __str__(self):
        status = "Positive" if self.is_glaucoma else "Negative"
        confidence = f"{self.confidence_score:.1f}%" if self.confidence_score is not None else "N/A"
        return f"Test for {self.patient.name} - {status} ({confidence})"
    
    def mark_processing(self):
        """Mark the test as being processed."""
        self.status = 'processing'
        self.save()
    
    def mark_completed(self, is_glaucoma, raw_score, confidence_score):
        """Mark the test as completed with results."""
        self.status = 'completed'
        self.is_glaucoma = is_glaucoma
        self.raw_score = raw_score
        self.confidence_score = confidence_score
        self.date_processed = timezone.now()
        self.processing_time = (self.date_processed - self.date_created).total_seconds()
        self.save()
    
    def mark_failed(self, error_message):
        """Mark the test as failed with an error message."""
        self.status = 'failed'
        self.error_message = error_message
        self.date_processed = timezone.now()
        self.save()
    
    @property
    def result_text(self):
        """Return a human-readable result."""
        if self.is_glaucoma is None:
            return "Not processed yet"
        return "Glaucoma Detected" if self.is_glaucoma else "Glaucoma Not Detected"
    
    @property
    def confidence_percent(self):
        """Return confidence as percentage string."""
        if self.confidence_score is None:
            return "N/A"
        return f"{self.confidence_score:.1f}%"