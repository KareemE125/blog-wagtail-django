from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
# Create your models here.

class BlogPage(Page):
    body = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        posts = self.get_children().live().order_by('-first_published_at')
        context["posts"] = posts
        return context
   
    
class PostPage(Page):
    date = models.DateField("Post date", auto_now_add=True)
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]
    
    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('intro'),
    ]