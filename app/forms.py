from django import forms
from .models import MediaFile


class MediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = ["file"]

    def clean_file(self):
        file = self.cleaned_data.get("file")
        if file:
            # Check file size (100KB to 10MB)
            if file.size < 100 * 1024:  # 100KB
                raise forms.ValidationError("File size must be at least 100KB")
            if file.size > 10 * 1024 * 1024:  # 10MB
                raise forms.ValidationError("File size must not exceed 10MB")

            # Get file extension
            extension = file.name.split(".")[-1].lower()
            if extension not in ["mp3", "mp4", "jpeg", "jpg", "png", "gif"]:
                raise forms.ValidationError("Invalid file type")
        return file
