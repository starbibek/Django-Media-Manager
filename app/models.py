from django.db import models
from django.core.validators import (
    FileExtensionValidator,
    MinValueValidator,
    MaxValueValidator,
)
import os


class MediaFile(models.Model):
    CATEGORY_CHOICES = [
        ("AUDIO", "Audio"),
        ("VIDEO", "Video"),
        ("IMAGE", "Image"),
    ]
    file = models.FileField(
        upload_to="files/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["mp3", "mp4", "jpeg", "png", "gif"]
            )
        ],
    )
    filename = models.CharField(max_length=255)
    size = models.IntegerField()  # Size in bytes
    file_type = models.CharField(max_length=10)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Delete the file from filesystem when model instance is deleted
    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)

    # method to fetch file category from extension type
    def get_file_category(self):
        extension = self.file_type.lower()
        if extension in ["mp3"]:
            return "AUDIO"
        elif extension in ["mp4"]:
            return "VIDEO"
        elif extension in ["jpeg", "jpg", "png", "gif"]:
            return "IMAGE"
        return None
