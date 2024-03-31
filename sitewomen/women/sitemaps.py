from django.contrib.sitemaps import Sitemap

from women.models import Category, Women

# для поисковых систем

class PostSitemap(Sitemap):
    changefreq = 'montly'
    priority = 0.9
    
    def items(self):
        return Women.published.all()
    
    def lastmod(self, obj: Women):
        return obj.time_update


class CategorySitemap(Sitemap):
    changefreq = 'montly'
    priority = 0.9
    
    def items(self):
        return Category.objects.all()
