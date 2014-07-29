from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from forms import DataImportForm
from models import DataImport


def delete_import(request, slug):
    im = get_object_or_404(DataImport, slug=slug)
    im.delete()
    messages.success(request,_("The record of the import was deleted. No data was not removed from MongoDB."))
    return HttpResponseRedirect(reverse('show_dbs'))
    


def import_data_file(request, database_name=None, collection_name=None):
    name = _("Import a Data File into a Mongo Database")
    
    
    if request.method == 'POST':
        form = DataImportForm(request.POST, request.FILES)
        if form.is_valid():
            di = form.save(commit = False)
            di.user = request.user
            di.save()
            messages.success(request,_("The data was imported successfully."))   
            return HttpResponseRedirect(reverse('show_dbs'))
        else:
            #The form is invalid
             messages.error(request,_("Please correct the errors in the form."))
             return render_to_response('generic/bootstrapform.html',
                                            {'form': form,
                                            'name':name, },
                                            RequestContext(request))
            
    #this is a GET
    
    print database_name, collection_name
    if database_name and collection_name:
                idata ={'database_name': database_name,
             'collection_name': collection_name,
             }
    

    else:
            idata ={'database_name': settings.MONGO_DB_NAME,
           'collection_name': settings.MONGO_MASTER_COLLECTION,
           }

    context= {'name':name,
              'form': DataImportForm(initial=idata)
              }
    return render_to_response('generic/bootstrapform.html',
                              RequestContext(request, context,))




def previous_data_imports(request, database_name=None, collection_name=None):
   
    if not database_name or collection_name:
        dataimports = DataImport.objects.filter(database_name=database_name,
                                            collection_name=database_name)
    else:
        dataimports = DataImport.objects.all()
            
    context = {"dataimports": dataimports }
    return render_to_response('dataimport/previous.html',
                              RequestContext(request, context,))