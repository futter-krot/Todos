from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from tasks.models import *
from datetime import datetime
from django.views.decorators.cache import cache_page
from django.db import IntegrityError

def index(request):

    # 1st version
    # counts = {t.name: random.randint(1, 100) for t in Tag.objects.all()}

    # 2nd version
    # counts = {t.name: t.taggit_taggeditem_items.count()
    # for t in Tag.objects.all()}

    # 3rd version
    from django.db.models import Count

    counterHigh = CounterHigh.objects.get(id=1)
    counterLow = CounterLow.objects.get(id=1)
    counterMedium = CounterMedium.objects.get(id=1)
    context = {
        'counterHigh': counterHigh,
        'counterLow': counterLow,
        'counterMedium': counterMedium
    }
    counts = Category.objects.annotate(total_tasks=Count(
        'todoitem')).order_by("-total_tasks")
    counts = {c.name: c.total_tasks for c in counts}
    return render(request, "tasks/index.html", {"counts": counts, 'c': context})


def filter_tasks(tags_by_task):
    return set(sum(tags_by_task, []))


def tasks_by_cat(request, cat_slug=None):
    u = request.user
    tasks = TodoItem.objects.filter(owner=u).all()

    cat = None
    if cat_slug:
        cat = get_object_or_404(Category, slug=cat_slug)
        tasks = tasks.filter(category__in=[cat])

    categories = []
    for t in tasks:
        for cat in t.category.all():
            if cat not in categories:
                categories.append(cat)

    return render(
        request,
        "tasks/list_by_cat.html",
        {"category": cat, "tasks": tasks, "categories": categories},
    )


class TaskListView(ListView):
    model = TodoItem
    context_object_name = "tasks"
    template_name = "tasks/list.html"

    def get_queryset(self):
        u = self.request.user
        qs = super().get_queryset()
        return qs.filter(owner=u)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_tasks = self.get_queryset()
        tags = []
        for t in user_tasks:
            tags.append(list(t.category.all()))

        categories = []
        for cat in t.category.all():
            if cat not in categories:
                categories.append(cat)
        context["categories"] = categories

        return context


class TaskDetailsView(DetailView):
    model = TodoItem
    template_name = "tasks/details.html"


def delete_queryset(request, queryset):
    # if TodoItem.category.through.objects.all().values()[0]['category_id'] == TodoItem.category.through.objects.all().values()[-1]['category_id']:
    # idle = TodoItem.category.through.objects.all().values()[0]['category_id']
    # c = 0
    # for i in TodoItem.category.through.objects.all().values():
    #     if i['category_id'] == idle:
    #         c += 1
    if len(queryset.values()) == 1:
        todos = Category.objects.filter(id=TodoItem.category.through.objects.all().values()[0]['category_id']).values()[0]['todos_count'] - len(queryset.values())
        try:
            if Category.objects.filter(id=TodoItem.category.through.objects.all().values()[1]['category_id']).exists():
                Category.objects.filter(id=Category.objects.filter(
                    id=TodoItem.category.through.objects.all().values()[1]['category_id']).values()[0]['id']).update(
                    todos_count=todos)
        except IndexError:
            pass
        try:
            Category.objects.filter(id=Category.objects.filter(id=TodoItem.category.through.objects.all().values()[0]['category_id']).values()[0]['id']).update(todos_count=todos)
        except IntegrityError:
            pass
    else:
        idle = TodoItem.category.through.objects.all().values()[0]['category_id']
        x = 0
        oid = 0
        for i in TodoItem.category.through.objects.all().values():
            if i['category_id'] == idle:
                x += 1
            else:
                oid = i['category_id']
        extodos = Category.objects.filter(id=TodoItem.category.through.objects.all().values()[0]['category_id']).values()[0]['todos_count'] - x
        y = len(queryset.values()) - x
        eytodos = Category.objects.filter(id=TodoItem.category.through.objects.all().values()[0]['category_id']).values()[0]['todos_count'] - y
        definition = x-y-eytodos
        Category.objects.filter(id=Category.objects.filter(id=idle).values()[0]['id']).update(todos_count=definition)
        Category.objects.filter(id=Category.objects.filter(id=oid).values()[0]['id']).update(todos_count=extodos)
    TodoItem.category.through.objects.all().delete()
    queryset.delete()


@cache_page(60 * 5)
def date(request):
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    return render(request, 'tasks/date.html', {'current_date': current_date, 'current_time': current_time})
