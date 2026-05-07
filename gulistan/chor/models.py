from django.db import models

class SharedContent(models.Model):
    content = models.TextField(blank=True, default="")
    updated_at = models.DateTimeField(auto_now=True)

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    filename = models.CharField(max_length=255)
    content = models.TextField(blank=True, default="") # For text display
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename
