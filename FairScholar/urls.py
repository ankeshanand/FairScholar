from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
import settings
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'FairScholar.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^about/', TemplateView.as_view(template_name='about.html')),
    url(r'^api/get_keyword/', 'fairscholar.views.get_keyword', name='get_keyword'),
    url(r'^results/', 'fairscholar.views.show_results', name='show_results'),
)
