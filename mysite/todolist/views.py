from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse

from .models import Task
from .submit import complete_task, edit_submission, save_submission


def index(request):
    # type of request: https://docs.djangoproject.com/en/1.11/ref/request-response/#httprequest-objects

    # type of request.POST: https://docs.python.org/3.5/library/stdtypes.html#dict

    # values in request.POST are of type str
    print(request.POST)
    print(type(request.POST))
    
    todo_list = Task.objects.all()
    waiting_todos = todo_list.filter(completed=False)
    tasks_done = todo_list.filter(completed=True)
    past_search_term = ""
    task_to_be_edited_text = ""

    for item_name in request.POST:
        item_value = request.POST[item_name]
        complete_prefix = 'complete_task_'
        delete_prefix = "delete_submission_"
        undo_prefix = "undo_complete_"
        edit_prefix = "edit_task_"
        
        if (item_name.startswith(complete_prefix)):
            task_id_str = item_name[len(complete_prefix):]
            id_to_complete = int(task_id_str)
            print (id_to_complete)
            Task.objects.filter(id=id_to_complete).update(completed = True)

        if (item_name.startswith(delete_prefix)):
            task_id_str = item_name[len(delete_prefix):]
            id_to_delete = int(task_id_str)
            print (id_to_delete)
            Task.objects.filter(id=id_to_delete).delete()

        if (item_name.startswith(undo_prefix)):
            task_id_str = item_name[len(undo_prefix):]
            id_to_undo = int(task_id_str)
            print (id_to_undo)
            Task.objects.filter(id=id_to_undo).update(completed = False)

        if (item_name.startswith("submit_task")):
            content = (request.POST['text_field'])
            if content != "":
                if not Task.objects.filter(task_text=content).exists():
                    save_submission(content)

        if (item_name.startswith("search_tasks")):
            content = (request.POST['text_field'])
            past_search_term = content
            if content != "":
                print(content)
                print(Task.objects.filter(task_text__icontains=content))
                waiting_todos = todo_list.filter(
                    task_text__icontains=content, completed=False)
                tasks_done = todo_list.filter(
                    task_text__icontains=content, completed=True)

        if (item_name.startswith(edit_prefix)):
            task_id_str = item_name[len(edit_prefix):]
            id_to_undo = int(task_id_str)
            task_to_edit_part1 = Task.objects.filter(id=id_to_undo)[0]
            task_to_be_edited_text = task_to_edit_part1.task_text

            # use the ID to fetch 

    # if request.POST.get("edit_task"):
    #     id_to_edit = (request.POST['task_id'])
    #     content = (request.POST['text_field'])
    #     print (id_to_edit)
    #     print (content)
    #     edit_submissions(id_to_edit)

    context = {
        'waiting_todos': waiting_todos,
        'tasks_done': tasks_done,
        'past_search_term': past_search_term,
        'task_to_be_edited_text': task_to_be_edited_text,
    }

    # print  (context)

    return render(request, 'todolist/index.html', context)
