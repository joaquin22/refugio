from django.shortcuts import render,redirect

from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy 
from django.core import serializers
from django.views.generic import ListView,CreateView,UpdateView,DeleteView


from apps.mascota.forms import Mascotaform
from apps.mascota.models import Mascota
# Create your views here.

def listado(request):
    lista = serializers.serialize('json',Mascota.objects.all())
    return HttpResponse(lista,content_type='application/json')


def index(request):
    return render(request,'mascota/index.html')

#Vistas en funciones
def mascota_view(request):
    if request.method == 'POST':
        form = Mascotaform(request.POST)
        if form.is_valid():
            form.save()
        return redirect('mascota:mascota_listar')
    else:
        form = Mascotaform()

    return render(request,'mascota/mascota_form.html',{'form':form})

def mascota_list(request):
    mascota = Mascota.objects.all().order_by('id')
    contexto ={'mascotas':mascota}
    return render(request,'mascota/mascota_list.html',contexto)

def mascota_edit(request,id_mascota):
    mascota = Mascota.objects.get(id = id_mascota)
    if request.method == 'GET':
        form = Mascotaform(instance=mascota)
    else:
        form = Mascotaform(request.POST,instance=mascota)
        if form.is_valid():
            form.save()  
        return redirect('mascota:mascota_listar')
    return render(request,'mascota/mascota_form.html',{'form':form})

def mascota_delete(request,id_mascota):
    mascota = Mascota.objects.get(id = id_mascota)
    if request.method == 'POST':
        mascota.delete()
        return redirect('mascota:mascota_listar')
    return render(request,'mascota/mascota_delete.html',{'mascota':mascota})


#Vistas en clases


class MascotaList(ListView):
    model = Mascota
    template_name = 'mascota/mascota_list.html'
    paginate_by = 1


class MascotaCreate(CreateView):
    model = Mascota
    form_class = Mascotaform
    template_name = 'mascota/mascota_form.html'
    success_url = reverse_lazy('mascota:mascota_listar')


class MascotaUpdate(UpdateView):
    model = Mascota
    form_class = Mascotaform
    template_name = 'mascota/mascota_form.html'
    success_url = reverse_lazy('mascota:mascota_listar')


class MascotaDelete(DeleteView):
    model = Mascota
    template_name = 'mascota/mascota_delete.html'
    success_url = reverse_lazy('mascota:mascota_listar')
