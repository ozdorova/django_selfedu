from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, Http404, HttpResponseRedirect, \
    HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, TemplateView, UpdateView

from .utils import DataMixin

from .forms import AddPostForm, UploadFileForm
from women.models import UploadFiles, Women, Category, TagPost
import uuid


# функции представления


class WomenHome(DataMixin, ListView):
    # model = Women
    #переопределние url страницы из ListView
    template_name = 'women/index.html'
    # переопределие object_list на posts в index.html
    context_object_name = 'posts'
    
    ##### Новые атрибуты для DataMixin в utils.py
    cat_selected = 0
    title_page = 'Главная страница'
    
    def get_queryset(self):
        return Women.published.all().select_related('cat')
    # extra_context = {
    #     'title': 'Главная страница',
    #     'menu': menu,
    #     'posts': Women.published.all().select_related('cat'),
    #     'cat_selected': 0,
    # } # переменные передаваемые в шаблон
    
    # def get_context_data(self, **kwargs: Any):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['menu'] = menu
    #     context['posts'] = Women.published.all().select_related('cat')
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #     return context


class ShowPost(DataMixin, DetailView):
    # model = Women
    template_name = 'women/post.html'
    
    # переменная которая фигурирует в маршруте urls
    slug_url_kwarg = 'post_slug'
    # по умолчанию переменная обращения object в post.hmtl
    context_object_name = 'post' # переорпределяет object в post
    
    def get_object(self, queryset=None):
        #отображение только опубликованных постов
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)
        
        # не нужно так как теперь определение дополнительных атрибутов для шаблона определяется в классе DataMixin
        # context['title'] = context['post'].title
        # context['menu'] = menu
        # return context


def about(request: HttpRequest):
    if request.method == 'POST':
        #загрузка файлов медиа
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(form.cleaned_data['file'])
            fp = UploadFiles(file=form.cleaned_data['file'])
            # загрузка файла с использованием модели
            fp.save()
    else:
        form = UploadFileForm()
        
    return render(request, 'women/about.html',
                {'title': 'О сайте', 'form': form}
                )


class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    # # или 
    # model = Women
    # fields = '__all__'
    
    title_page = 'Добавление статьи' # DataMixin
    template_name = 'women/addpage.html'
    
    # атрибут который отвечает адрес переотправки послу успешного заполнения формы
    # reverse_lazy получает полный адрес машрута по имени в момент когда необходимо, а не в момент определения
    # success_url = reverse_lazy('home')
    # в  СreateView не нужен success_url если в форме или в модели определен метод get_absolute_url
    
    # extra_context = {
    #     'menu': menu,
    #     'title': 'Добавление статьи',
    # }


class UpdatePage(DataMixin, UpdateView):
    # обновление поста
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    
    title_page = 'Редактирование статьи'
    


class DeletePage(DataMixin, DeleteView):
    # удаление поста
    model = Women
    template_name = 'women/delete.html'
    
    success_url = reverse_lazy('home')
    title_page = 'Удаление статьи'
    

    
    # Реализован в классе CreateView
    # def form_valid(self, form):
    #     # вызывается только если форма была заполнена корректно
    #     form.save()
    #     return super().form_valid(form)


def contact(request: HttpRequest):
    return HttpResponse('Обратная связь')


def login(request: HttpRequest):
    return HttpResponse('Авторизация')


class WomenCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    # генерируется 404 при пустом списке (когда указывается неверный слаг)
    allow_empty = False
    
    def get_queryset(self):
        #Ключ cat_slug автоматически формируется по шаблону маршрута (файл women/urls.py)
        # фильтрация постов по слагу, то есть по категориям
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        # cat из первой записи которая будет отображаться
        # # вместо
        # cat = context['posts'][0].cat
        # # используем
        # cat = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        cat = context['posts'][0].cat
        return self.get_mixin_context(
            context,
            title='Категория -' + cat.name,
            cat_selected=cat.pk,
        )


class TagPostList(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False
    
    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        # tag = context['posts'][0].tags.all()[0]
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(
            context,
            title=f'Тег -{tag.tag}',
        )
    
    

    # template_name = 'women/index.html'
    # context_object_name = 'posts'
    # allow_empty = False

    # def get_queryset(self):
    #     return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     tag = context['posts'][0].tags.all()[0]
    #     context['title'] = f'Тег - {tag.tag}'
    #     context['menu'] = menu
    #     context['cat_selected'] = None
    #     return context
    
def page_not_found(request: HttpRequest, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")