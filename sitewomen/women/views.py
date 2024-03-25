from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, Http404, HttpResponseRedirect, \
    HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import DetailView, FormView, ListView, TemplateView

from .forms import AddPostForm, UploadFileForm
from women.models import UploadFiles, Women, Category, TagPost
import uuid


# функции представления


menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page' }, 
    {'title': "Обратная связь", 'url_name': 'contact'}, 
    {'title': "Войти", 'url_name': 'login'},
]


# временный словарь для проверки
# data_db = [
    
#     {'id': 1, 'title': 'Анджелина Джоли', 'content': '''<h1>Анджелина Джоли</h1> (англ. Angelina Jolie[7], при рождении Войт (англ. Voight), ранее Джоли Питт (англ. Jolie Pitt); род. 4 июня 1975, Лос-Анджелес, Калифорния, США) — американская актриса кино, телевидения и озвучивания, кинорежиссёр, сценаристка, продюсер, фотомодель, посол доброй воли ООН.
    
#     Обладательница премии «Оскар», трёх премий «Золотой глобус» (первая актриса в истории, три года подряд выигравшая премию) и двух «Премий Гильдии киноактёров США».''',
#     'is_published': True},
    
#     {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
#     {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулии Робертс', 'is_published': True},
# ]

# cats_db = [
#     {'id': 1, 'name': 'Актрисы'},
#     {'id': 2, 'name': 'Певицы'},
#     {'id': 3, 'name': 'Спортсменки'},
# ]


# def index(request: HttpRequest): # HttpRequest
#     # t = render_to_string('women/index.html') # рендер шаблона
#     # return HttpResponse(t)
#     posts = Women.published.all().select_related('cat')
    
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     } # переменные передаваемые в шаблон

#     return render(request=request, template_name='women/index.html', context=data) # лучше делать так


class WomenHome(ListView):
    # model = Women
    #переопределние url страницы из ListView
    template_name = 'women/index.html'
    # переопределие object_list на posts в index.html
    context_object_name = 'posts'
    # обьявление статических данных которые активны только при обьявлении класса
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
    } 
    
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


def show_post(request: HttpRequest, post_slug):
    # Читаем одну модель по ключевому ключу из модели БД
    post = get_object_or_404(Women, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    
    return render(request, 'women/post.html', data)


class ShowPost(DetailView):
    # model = Women
    template_name = 'women/post.html'
    
    # переменная которая фигурирует в маршруте urls
    slug_url_kwarg = 'post_slug'
    # по умолчанию переменная обращения object в post.hmtl
    context_object_name = 'post' # переорпределяет object в post
    
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        return context
    
    def get_object(self, queryset=None):
        #отображение только опубликованных постов
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])
    
    
    
    
    
# def handle_uploaded_file(f):
#     #функция для записи файлов
#     unique_filename = str(uuid.uuid4()) # уникальное имя ф
#     with open(f'uploads/{unique_filename}_{f.name}', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


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
                {'title': 'О сайте', 'menu': menu, 'form': form}
                )


# def addpage(request: HttpRequest):
#     if request.method == 'POST':
#         #request.POST - полученные данные
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # # проверка корректности данных
#             # print(form.cleaned_data)
#             # try:
#             #     # Добавление полученных данных с формы в БД
#             #     Women.objects.create(**form.cleaned_data)
#             #     #Перенаправление на главную страницу
#             #     return redirect('home')
#             # except Exception as err:
#             #     # Если произошла ошибка
#             #     form.add_error(None, err)
            
#             form.save()
#             return redirect('home')
#     else:
#         # GET
#         form = AddPostForm()
    
#     data = {
#         'title': 'Добавление статьи',
#         'menu': menu,
#         'form': form,
#     }
#     return render(request, 'women/addpage.html', data)



class AddPage(FormView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    # атрибут который отвечает адрес переотправки послу успешного заполнения формы
    # reverse_lazy получает полный адрес машрута по имени в момент когда необходимо, а не в момент определения
    success_url = reverse_lazy('home')
    extra_context = {
        'menu': menu,
        'title': 'Добавление статьи',
    }
    
    def form_valid(self, form):
        # вызывается только если форма была заполнена корректно
        form.save()
        return super().form_valid(form)



# class AddPage(View):
#     # http_method_names = [
#     #     "get",
#     #     "post",
#     #     "put",
#     #     "patch",
#     #     "delete",
#     #     "head",
#     #     "options",
#     #     "trace",
#     # ]
    
#     def get(self, request):
#         form = AddPostForm()
#         data = {
#             'title': 'Добавление статьи',
#             'menu': menu,
#             'form': form,
#         }
        
#         return render(request, 'women/addpage.html', data)
    
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')

#         data = {
#             'title': 'Добавление статьи',
#             'menu': menu,
#             'form': form,
#         }
        
#         return render(request, 'women/addpage.html', data)


def contact(request: HttpRequest):
    return HttpResponse('Обратная связь')


def login(request: HttpRequest):
    return HttpResponse('Авторизация')


# def show_category(request: HttpRequest, cat_slug):
#     #отдельная запись из таблиц категорий
#     category = get_object_or_404(Category, slug=cat_slug)
#     # постыc
#     posts = Women.published.filter(cat_id=category.pk).select_related('cat')
    
#     data = {
#         'title': f'Рубрика: {category.name}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': category.pk,
#     } # переменные передаваемые в шаблон
#     return render(request, 'women/index.html', context=data)


class WomenCategory(ListView):
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
        context['title'] = 'Категория -' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context
    
    
    

# def show_tag_postlist(request: HttpRequest, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
    
#     posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')
    
#     data = {
#         'title': f"Тег: {tag.tag}",
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
    
#     return render(request, 'women/index.html', context=data)


class TagPostList(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False
    
    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        
        # tag = context['posts'][0].tags.all()[0]
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = f'Тег -{tag.tag}'
        context['menu'] = menu
        context['cat_selected'] = None
        return context
    
    

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


# def categories(request: HttpRequest, cat_id):
#     return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {cat_id}</p>")


# def categories_by_slug(request: HttpRequest, cat_slug):
#     if request.POST: # GET
#         print(request.POST)
#     return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>")





# def archive(request: HttpRequest, year):
#     if year > 2024:
#         uri = reverse('cats', args=('sport',)) # возращает вычисленный url адрес, args параметры машрута

#         # return HttpResponseRedirect('/') # 301
#         # return HttpResponsePermanentRedirect('/') # 301

#         return redirect(uri)

#         # return redirect('cats', 'music')# перенаправление по имени. Рекомендуется. music - значение передаваемая
#         # функции представления cats_slug

#     return HttpResponse(f"<h1>Архив по годам</h1><p>year: {year}</p>")
#     # return redirect('/', permanent=True) # адрес главной страницы, permanent=True - код 301, False - код 302
#     # return redirect(index) # перенаправление по функции представления

