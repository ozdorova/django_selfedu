from django.urls import path, re_path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.WomenHome.as_view(), name='home'), # http://127.0.0.1:8000/
    path('about/', views.about, name='about'), #http://127.0.0.1:8000/about/
    path('addpage/', views.AddPage.as_view(), name="add_page"),
    path('contact/', views.contact, name="contact"),
    path('login/', views.login, name="login"),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name="post"),
    path('category/<slug:cat_slug>/', views.WomenCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
]


    # path('cats/<int:cat_id>/', views.categories, name='cats_id'), # http://127.0.0.1:8000/cats/2/
    # path('cats/<slug:cat_slug>/', views.categories_by_slug, name='cats'), # http://127.0.0.1:8000/cats/sdfggd/
    # path("archive/<year4:year>", views.archive, name='archive')  # name - маршрут обращения

# машрут.                      функция представления, имя обращения
# path('tag/<slug:tag_slug>/', views.show_tag_postlist, name=tag)
# машрут связан с отображением тегов

#TagPost
# Возращает url адрес для тега
# def get_absolute_url(self):
#         return reverse("tag", kwargs={"tag_slug": self.slug})
