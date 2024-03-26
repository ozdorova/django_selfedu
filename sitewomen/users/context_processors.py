from women.utils import menu

# контекстный процессор
# передает menu по умолчанию в каждый шаблон, до этого menu передавалось через views, затем через utils
def get_women_context(request):
    return {'mainmenu': menu}