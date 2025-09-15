from http import HTTPStatus
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.api.serializers import *
from drf_spectacular.utils import extend_schema

try:
    from apps.common.models import Sales
except:
    pass

class SalesListCreateView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = SalesSerializer

    @extend_schema(operation_id='sales_list', responses=SalesSerializer)
    def get(self, request):
        return Response({
            'data': [SalesSerializer(instance=obj).data for obj in Sales.objects.all()],
            'success': True
        }, status=HTTPStatus.OK)

    @extend_schema(operation_id='sales_create', request=SalesSerializer, responses=SalesSerializer)
    def post(self, request):
        serializer = SalesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={
                **serializer.errors,
                'success': False
            }, status=HTTPStatus.BAD_REQUEST)
        serializer.save()
        return Response(data={
            'message': 'Record Created.',
            'success': True
        }, status=HTTPStatus.OK)


class SalesDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = SalesSerializer

    @extend_schema(operation_id='sales_retrieve', responses=SalesSerializer)
    def get(self, request, pk):
        try:
            obj = get_object_or_404(Sales, pk=pk)
        except Http404:
            return Response(data={
                'message': 'object with given id not found.',
                'success': False
            }, status=HTTPStatus.NOT_FOUND)
        return Response({
            'data': SalesSerializer(instance=obj).data,
            'success': True
        }, status=HTTPStatus.OK)

    @extend_schema(operation_id='sales_update', request=SalesSerializer, responses=SalesSerializer)
    def put(self, request, pk):
        try:
            obj = get_object_or_404(Sales, pk=pk)
        except Http404:
            return Response(data={
                'message': 'object with given id not found.',
                'success': False
            }, status=HTTPStatus.NOT_FOUND)
        serializer = SalesSerializer(instance=obj, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(data={
                **serializer.errors,
                'success': False
            }, status=HTTPStatus.BAD_REQUEST)
        serializer.save()
        return Response(data={
            'message': 'Record Updated.',
            'success': True
        }, status=HTTPStatus.OK)

    @extend_schema(operation_id='sales_destroy')
    def delete(self, request, pk):
        try:
            obj = get_object_or_404(Sales, pk=pk)
        except Http404:
            return Response(data={
                'message': 'object with given id not found.',
                'success': False
            }, status=HTTPStatus.NOT_FOUND)
        obj.delete()
        return Response(data={
            'message': 'Record Deleted.',
            'success': True
        }, status=HTTPStatus.OK)

