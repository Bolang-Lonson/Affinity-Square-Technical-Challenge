from django.db import models

# Create your models here.
class ParseLog(models.Model):
    url = models.URLField()
    html_version = models.CharField(max_length=10)
    page_title = models.CharField(max_length=255)
    num_headings = models.JSONField()  # Store as JSON: {'h1': 2, 'h2': 4, ...}
    num_links = models.JSONField()  # Store as JSON: {'internal': 10, 'external': 5}
    has_login_form = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

