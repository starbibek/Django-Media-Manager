from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, FileResponse
from django.contrib import messages
from .models import MediaFile
from .forms import MediaFileForm


def index(request):
    files = MediaFile.objects.all().order_by("-uploaded_at")
    return render(request, "media_manager/index.html", {"files": files})


def upload_file(request):
    if request.method == "POST":
        files = request.FILES.getlist("file")

        if len(files) > 10:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Cannot upload more than 10 files at once",
                }
            )

        success_count = 0
        error_messages = []

        for file in files:
            form = MediaFileForm(request.POST, {"file": file})
            if form.is_valid():
                media = MediaFile(
                    file=file,
                    filename=file.name,
                    size=file.size,
                    file_type=file.name.split(".")[-1].lower(),
                )
                media.category = media.get_file_category()
                media.save()
                success_count += 1
            else:
                error_messages.append(
                    f'Error uploading {file.name}: {form.errors["file"][0]}'
                )

        if success_count > 0:
            message = f"Successfully uploaded {success_count} file(s)"
            if error_messages:
                message += f". Errors: {', '.join(error_messages)}"
            return JsonResponse(
                {
                    "success": True,
                    "message": message,
                    "files": list(
                        MediaFile.objects.all().order_by("-uploaded_at").values()
                    ),
                }
            )
        else:
            return JsonResponse(
                {"success": False, "message": ". ".join(error_messages)}
            )

    return JsonResponse({"success": False, "message": "Invalid request method"})


def delete_file(request, pk):
    if request.method == "POST":
        try:
            media = MediaFile.objects.get(pk=pk)
            media.delete()
            return JsonResponse(
                {
                    "success": True,
                    "message": "File deleted successfully",
                    "files": list(
                        MediaFile.objects.all().order_by("-uploaded_at").values()
                    ),
                }
            )
        except MediaFile.DoesNotExist:
            return JsonResponse(
                {
                    "success": False,
                    "message": "File not found or already deleted",
                    "files": list(
                        MediaFile.objects.all().order_by("-uploaded_at").values()
                    ),
                },
                status=404,
            )
        except Exception as e:
            return JsonResponse(
                {
                    "success": False,
                    "message": f"Error deleting file: {str(e)}",
                    "files": list(
                        MediaFile.objects.all().order_by("-uploaded_at").values()
                    ),
                },
                status=500,
            )
    return JsonResponse(
        {"success": False, "message": "Invalid request method"}, status=405
    )


def download_file(request, pk):
    try:
        media = MediaFile.objects.get(pk=pk)
        try:
            # Check if file exists first
            if not media.file or not media.file.storage.exists(media.file.name):
                return JsonResponse(
                    {"success": False, "message": "File not found on server"},
                    status=404,
                )

            # If file exists, stream it
            response = FileResponse(media.file, as_attachment=True)
            response["Content-Disposition"] = f'attachment; filename="{media.filename}"'
            response["X-Sendfile"] = media.file.path
            return response

        except Exception as e:
            return JsonResponse(
                {"success": False, "message": f"Error downloading file: {str(e)}"},
                status=500,
            )
    except MediaFile.DoesNotExist:
        return JsonResponse(
            {"success": False, "message": "File record not found"}, status=404
        )
