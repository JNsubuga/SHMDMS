from django.utils import timezone

API_URL = "http://localhost:8000/api"

# Required Image Extensions
valid_image_extensions = [".jpg", ".png"]

# Thumbmnail path
# thumbnails_path = "media/images/thumbnails/"
thumbnails_path = "media/images/"

image_dir_indent = "thumbs"

############
# PAGINATION
############

results_per_page = 25


default_date_time = timezone.now()
