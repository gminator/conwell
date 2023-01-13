from django.shortcuts import render
from django.views.generic import TemplateView
import socket
from game.models import Grid
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status,viewsets

class WebNodeView(TemplateView):
    template_name = "play/webnode.html"

    def get_context_data(self, **kwargs):
       context = super(WebNodeView, self).get_context_data(**kwargs)
       
       context["hostname"] = socket.gethostname()
       context["ip_address"] = socket.gethostbyname( context["hostname"])
       context["game"] = Grid(30,10, 20, None, 100).run(True)
       return context

class ApiView(viewsets.ViewSet):
	#authentication_classes = [authentication.TokenAuthentication]
	#permission_classes = (permissions.IsAuthenticated,) 

	def create(self, request):
		hostname = socket.gethostname()
		return Response({
			"host" : hostname,
			"ip" : socket.gethostbyname(hostname)
		})