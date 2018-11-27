from kindergarden.models.bases import *
from kindergarden.lib import generic


class OrganisationCreate(generic.GenericView):
    model = Organisation
    form = generic.GenericForm(model=model)



