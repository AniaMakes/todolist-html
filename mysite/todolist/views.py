from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse

from .models import Task
from .submit import  save_submission, edit_submission, complete_task



def index(request):
    print(request.POST)
    todo_list = Task.objects.all()
    waiting = todo_list.filter(completed=False)
    done = todo_list.filter(completed=True)
    

    if request.POST.get("submit_task"):
        content = (request.POST['text_field'])
        if content != "":
            if not Task.objects.filter(task_text=content).exists():
                save_submission(content)

    if request.POST.get("complete_task"):
        id_to_complete = (request.POST['task_id'])
        print (id_to_complete)
        # complete_task(id_to_complete)
        Task.objects.filter(id=id_to_complete).update(completed = True)
    
    if request.POST.get("delete_submission"):
        id_to_complete = (request.POST['task_id'])
        print (id_to_complete)
        print (Task.objects.filter(id=id_to_complete))
        Task.objects.filter(id=id_to_complete).delete()

    if request.POST.get("undo_complete"):
        id_to_complete = (request.POST['task_id'])
        print (id_to_complete)
        # complete_task(id_to_complete)
        Task.objects.filter(id=id_to_complete).update(completed = False)
    
    # if request.POST.get("edit_task"):
    #     id_to_edit = (request.POST['task_id'])
    #     content = (request.POST['text_field'])
    #     print (id_to_edit)
    #     print (content)        
    #     edit_submissions(id_to_edit)
          
    if request.POST.get("search_tasks"):
        content = (request.POST['text_field'])

        if content != "":  
            print (content)            
            print (Task.objects.filter(task_text__icontains=content))
            waiting = todo_list.filter(task_text__icontains=content)
            done = todo_list.filter(task_text__icontains=content, completed=True)
    
    context = {
        'waiting': waiting,
        'done' : done, 
    }
    return render(request, 'todolist/index.html', context)

