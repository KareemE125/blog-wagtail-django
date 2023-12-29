from django.db import models
from django import forms
from django.utils import timezone

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
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
    date = models.DateField("Post date", default=timezone.now, editable=True)
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    authors = ParentalManyToManyField('blog.Author', blank=True)
    
    def main_image(self):
        firstImage = self.gallery_images.first()
        if firstImage:
            return firstImage.image
        else:
            return None
        
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('authors', widget=forms.CheckboxSelectMultiple),    
        ], heading="Post information"),
        FieldPanel('body'),
        FieldPanel('intro'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]


@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')   
            
    panels = [
        FieldPanel('name'),
        FieldPanel('image'),
    ]
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Authors'
        
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Author, self).save(*args, **kwargs)
        
class PostPageGalleryImage(Orderable):
    page = ParentalKey(PostPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField(blank=True, max_length=250)
    
    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]
    