"""
Create or customize your page models here.
"""

from coderedcms.blocks import NAVIGATION_STREAMBLOCKS, BaseBlock
from coderedcms.fields import CoderedStreamField
from django.db import models
from django.shortcuts import redirect, render
from modelcluster.fields import ParentalKey
from coderedcms.forms import CoderedFormField
from coderedcms.models import (
    CoderedArticlePage,
    CoderedArticleIndexPage,
    CoderedEmail,
    CoderedFormPage,
    CoderedWebPage,
)
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting, BaseSetting
from wagtail.fields import StreamField
from wagtail.images import get_image_model_string
from wagtail.models import TranslatableMixin, Orderable
from wagtail.snippets.models import register_snippet

from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image

from website.blocks import CUSTOM_CONTENT_STREAMBLOCKS, CUSTOM_LAYOUT_STREAMBLOCKS
from django.db import models
from coderedcms.models import CoderedPage
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.documents.models import Document
from .forms import DocumentUploadForm
import pdb


class ArticlePage(CoderedArticlePage):
    """
    Article, suitable for news or blog content.
    """

    class Meta:
        verbose_name = "Article"
        ordering = ["-first_published_at"]

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ["website.ArticleIndexPage"]

    template = "coderedcms/pages/article_page.html"
    search_template = "coderedcms/pages/article_page.search.html"

    body = StreamField(
        CUSTOM_CONTENT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )


class ArticleIndexPage(CoderedArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """

    class Meta:
        verbose_name = "Article Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.ArticlePage"

    # Only allow ArticlePages beneath this page.
    subpage_types = ["website.ArticlePage"]

    template = "coderedcms/pages/article_index_page.html"

    body = StreamField(
        CUSTOM_LAYOUT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )


class LocationPage(CoderedArticlePage):
    class Meta:
        verbose_name = "Location"
        ordering = ["-first_published_at"]

    parent_page_types = ["website.LocationIndexPage"]
    template = "coderedcms/pages/location_page.html"
    search_template = "coderedcms/pages/location_page.search.html"

    body = StreamField(
        CUSTOM_LAYOUT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )

    address = models.CharField(max_length=255, blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    thumbnail = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Thumbnail image",
    )

    content_panels = CoderedArticlePage.content_panels + [
        FieldPanel("address"),
        FieldPanel("tel"),
        FieldPanel("thumbnail"),
    ]


class LocationIndexPage(CoderedArticleIndexPage):
    class Meta:
        verbose_name = "Location Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.LocationPage"

    # Only allow ArticlePages beneath this page.
    subpage_types = ["website.LocationPage"]

    template = "coderedcms/pages/location_index_page.html"

    body = StreamField(
        CUSTOM_LAYOUT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )


class FormPage(CoderedFormPage):
    """
    A page with an html <form>.
    """

    class Meta:
        verbose_name = "Form"

    template = "coderedcms/pages/form_page.html"


class FormPageField(CoderedFormField):
    """
    A field that links to a FormPage.
    """

    class Meta:
        ordering = ["sort_order"]

    page = ParentalKey("FormPage", related_name="form_fields")


class FormConfirmEmail(CoderedEmail):
    """
    Sends a confirmation email after submitting a FormPage.
    """

    page = ParentalKey("FormPage", related_name="confirmation_emails")


class WebPage(CoderedWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    """

    class Meta:
        verbose_name = "Web Page"

    template = "coderedcms/pages/web_page.html"

    body = StreamField(
        CUSTOM_LAYOUT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )


@register_snippet
class TranslateNavbar(TranslatableMixin, models.Model):
    """
    Snippet for site navigation bars (header, main menu, etc.)
    """
    name = models.CharField(
        max_length=255,
        verbose_name="Name",
    )
    custom_css_class = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Custom CSS Class",
    )
    custom_id = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Custom ID",
    )
    menu_items = CoderedStreamField(
        NAVIGATION_STREAMBLOCKS,
        verbose_name="Navigation links",
        blank=True,
        use_json_field=True,
    )

    panels = [
        FieldPanel("name"),
        MultiFieldPanel(
            [
                FieldPanel("custom_css_class"),
                FieldPanel("custom_id"),
            ],
            heading="Attributes",
        ),
        FieldPanel("menu_items"),
    ]

    def __str__(self):
        return self.name


@register_setting(icon="cr-desktop")
class CustomSetting(ClusterableModel, BaseSiteSetting):
    """
    Tracking and Google Analytics.
    """

    class Meta:
        verbose_name = "Custom Settings"

    captcha = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="captcha key",
        help_text='Your captcha site key'
        ,
    )
    language_menu = models.BooleanField(
        default=True,
        verbose_name="language menu item",
        help_text="Show/hide language menu item"
    )
    content_margin_top = models.IntegerField(
        default=0,
        verbose_name="content margin top (px)",
        help_text="margin top for content, use with fixed navbar settings"
    )
    footer_bg_color = models.CharField(
        null=True, blank=True, max_length=500,
        verbose_name="footer background color",
        help_text="footer background color value"
    )
    footer_text_color = models.CharField(
        null=True, blank=True, max_length=500,
        verbose_name="Footer text color",
        help_text="Footer text color value"
    )
    nav_bg_color = models.CharField(
        null=True, blank=True, max_length=500,
        verbose_name="Navbar background color",
        help_text="Navbar background color value"
    )

    facebook_page_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="facebook page id",
        help_text='Your facebook page id',
    )

    using_messenger = models.BooleanField(
        default=True,
        verbose_name="using facebook messenger chat support",
        help_text="Show/hide facebook messenger chat support"
    )

    whatsapp_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="whatsapp id",
        help_text='Your whatsapp id',
    )

    using_whatsapp = models.BooleanField(
        default=True,
        verbose_name="using whatsapp chat support",
        help_text="Show/hide whatsapp chat support"
    )
    email_host = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="EMAIL_HOST",
        help_text='Your Email Host',
    )
    email_port = models.PositiveIntegerField(
        default=0,
        verbose_name="EMAIL_PORT",
        help_text='Your Email Port',
    )
    email_use_tls = models.BooleanField(
        default=True,
        verbose_name="EMAIL_USE_TLS",
        help_text='Your Email Use TLS',
    )
    email_host_user = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="EMAIL_HOST_USER",
        help_text="Your Email Host User"
    )
    email_host_password = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="EMAIL_HOST_PASSWORD",
        help_text='Your Email Host Password',
    )
    email_sender = models.EmailField(
        null=True,
        verbose_name="Email Sender",
        help_text="Your email sender"
    )
    owner_mail = models.EmailField(
        null=True,
        verbose_name="Owner Mail",
        help_text="Owner Mail"
    )

    custom_css = models.TextField(
        null=True,
        verbose_name="Custom CSS",
        help_text="Custom CSS"
    )
    panels = [
        FieldPanel("captcha"),
        FieldPanel("language_menu"),
        FieldPanel("content_margin_top"),
        FieldPanel("nav_bg_color"),
        FieldPanel("footer_bg_color"),
        FieldPanel("footer_text_color"),
        FieldPanel("facebook_page_id"),
        FieldPanel("using_messenger"),
        FieldPanel("whatsapp_id"),
        FieldPanel("using_whatsapp"),
        FieldPanel("email_host"),
        FieldPanel("email_port"),
        FieldPanel("email_use_tls"),
        FieldPanel("email_host_user"),
        FieldPanel("email_host_password"),
        FieldPanel("email_sender"),
        FieldPanel("owner_mail"),

        InlinePanel(
            "site_navbartrans",
            help_text="Choose one or more navbars for your site.",
            heading="Site Navbars",
        ),
        FieldPanel("custom_css"),
    ]


class TransNavbarOrderable(Orderable, models.Model):
    navbar_chooser = ParentalKey(
        CustomSetting,
        related_name="site_navbartrans",
        verbose_name="Site Navbars",
    )
    navbar = models.ForeignKey(
        TranslateNavbar,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel("navbar")]


@register_snippet
class LocationMarker(models.Model):
    location = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    tel = models.CharField(max_length=20, help_text="Enter phone number in the format +1234567890")
    description = models.CharField(max_length=255, default='', verbose_name="Address")
    link = models.URLField(blank=True, null=True, help_text="Enter a link associated with this location")

    panels = [
        FieldPanel('location'),
        FieldPanel('latitude'),
        FieldPanel('longitude'),
        FieldPanel('tel'),
        FieldPanel('description'),
        FieldPanel('link'),
    ]

    def __str__(self):
        return self.location

    class Meta:
        verbose_name = "Location Marker"


@register_setting
class NavbarSettings(BaseSetting):
    navbar_transparent = models.BooleanField(default=False, help_text="Make the navbar transparent")

    panels = [
        FieldPanel('navbar_transparent'),
    ]


class DocumentManagementPage(CoderedPage):
    """
    A page type for managing documents.
    """
    template = 'website/document_management_page.html'

    # Add any additional fields you need
    intro = models.TextField(blank=True)

    content_panels = CoderedPage.content_panels + [
        FieldPanel('intro'),
    ]

    class Meta:
        verbose_name = "Document Management Page"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['documents'] = Document.objects.all()
        return context


    def serve(self, request):
        if request.method == 'POST':
            form = DocumentUploadForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect(self.url)
        else:
            form = DocumentUploadForm()
        
        context = self.get_context(request)
        context['form'] = form
        return render(request, self.template, context)


# training data page inherits from Documentmanagement Page

class DownloadDataPage(DocumentManagementPage):
    """
    A page for downloading documents only.
    """
    template = 'website/download_data_page.html'

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        return context

    class Meta:
        verbose_name = "Download Data Page"