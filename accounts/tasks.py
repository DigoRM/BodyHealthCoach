from celery import shared_task

@shared_task
def resize_and_upload_image(image):
    # Image resizing and uploading logic goes here
    # ...

    return 'Image resized and uploaded successfully'
