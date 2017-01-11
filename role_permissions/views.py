from django.views import View


class PermissionView(View):

    def get(self, request):
        pass


class RoleView(View):

    def get(self, request):
        pass

    def post(self, request):
        pass


class RoleDetailView(View):

    def get(self, request, pk):
        pass

    def delete(self, request, pk):
        pass
