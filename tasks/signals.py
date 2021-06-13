from django.db.models.signals import m2m_changed, post_save, post_delete
from django.dispatch import receiver
from tasks.models import TodoItem, Category


# @receiver(m2m_changed, sender=TodoItem.category.through)
# def task_cats_added(sender, instance, action, model, **kwargs):
#     if action != 'post_add':
#         return
#     cater = instance.category.values()
#     list_result = [entry for entry in cater]
#     listr = list_result[0]['todos_count']
#     listr += 1
#     Category.objects.filter(name=list_result[0]['name']).update(todos_count=listr)
#
#
# @receiver(m2m_changed, sender=TodoItem.category.through)
# def task_cats_removed(sender, instance, action, model, **kwargs):
#     if action != 'post_delete': #Eсли не работает, то попробуйте заменить post_delete на post_remove, возможно проблема в файлах миграций. На тесте всё работало.
#         return
#     cater = instance.category.values()
#     list_result = [entry for entry in cater]
#     listr = list_result[0]['todos_count']
#     listr -= 1
#     Category.objects.filter(name=list_result[0]['name']).update(todos_count=listr)


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats(sender, instance, action, model, **kwargs):
    if action == 'post_remove':
        cater = instance.category.values()
        list_result = [entry for entry in cater]
        try:
            listr = list_result[0]['todos_count']
            listr -= 1
            Category.objects.filter(name=list_result[0]['name']).update(todos_count=listr)
        except IndexError:
            pass
    elif action == 'post_add':
        cater = instance.category.values()
        list_result = [entry for entry in cater]
        try:
            listr = list_result[0]['todos_count']
            listr += 1
            Category.objects.filter(name=list_result[0]['name']).update(todos_count=listr)
        except IndexError:
            pass
    else:
        return


@receiver(post_save, sender=TodoItem)
def count_cats_added(instance, **kwargs):
    doH = instance.doH
    doL = instance.doL
    doM = instance.doM
    if instance.priority == 1:
        doH.counts += 1
        doH.save()
    elif instance.priority == 2:
        doM.counts += 1
        doM.save()
    else:
        doL.counts += 1
        doL.save()


@receiver(post_delete, sender=TodoItem)
def count_cats_removed(instance, **kwargs):
    doH = instance.doH
    doL = instance.doL
    doM = instance.doM
    if instance.priority == 1:
        doH.counts -= 1
        doH.save()
    elif instance.priority == 2:
        doM.counts -= 1
        doM.save()
    else:
        doL.counts -= 1
        doL.save()




