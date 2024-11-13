from django.shortcuts import render
from django.http import HttpResponse
from .forms import ExampleForm
# Create your views here.
@permission_required('bookshelf.can_edit', raise_exception=True)
def EditView(request):
    return HttpResponse('you can edit')

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    return HttpResponse('you can view')

@permission_required('bookshelf.can_create', raise_exception=True)
def CreateView(request):
    return HttpResponse('you can create')

@permission_required('bookshelf.can_delete', raise_exception=True)
def DeleteView(request):
    return HttpResponse('you can delete')

def exampleview(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        form.save()
    else:
        form = ExampleForm()
        return render(request, 'bookshelf/form_example.html', {'form': form})