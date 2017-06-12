from django import forms

class CreateTask(forms.Form):
    text_field_entry_create = forms.CharField(max_length=200)

class SearchTasks(forms.Form):
    text_field_entry_search = forms.CharField(max_length=200)
    
class EditTask (forms.Form):
    text_field_entry_edit = forms.CharField(max_length=200)
