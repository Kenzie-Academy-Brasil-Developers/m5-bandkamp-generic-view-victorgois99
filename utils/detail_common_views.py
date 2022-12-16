from rest_framework.views import APIView, Request, Response, status
from django.shortcuts import get_object_or_404


class GetDetailView:
    def retrieve(self, request: Request, pk: int) -> Response:

        model_object = get_object_or_404(self.view_queryset, pk=pk)

        self.check_object_permissions(request, model_object)

        serializer = self.view_serializer(model_object)

        return Response(serializer.data)


class PatchDetailView:
    def update(self, request: Request, pk: int) -> Response:

        model_object = get_object_or_404(self.view_queryset, pk=pk)

        self.check_object_permissions(request, model_object)

        serializer = self.view_serializer(model_object, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class DeleteDetailView:
    def destroy(self, request: Request, pk: int) -> Response:

        model_object = get_object_or_404(self.view_queryset, pk=pk)

        self.check_object_permissions(request, model_object)

        model_object.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class OnlyGetDetailView(GetDetailView, APIView):
    def get(self, request: Request, pk: int) -> Response:
        return super().retrieve(request, pk)


class OnlyPatchDetailView(PatchDetailView, APIView):
    def patch(self, request: Request, pk: int) -> Response:
        return super().update(request, pk)


class OnlyDeleteDetailView(DeleteDetailView, APIView):
    def delete(self, request: Request, pk: int) -> Response:
        return super().destroy(request, pk)


class GetPatchDeleteDetailView(
    GetDetailView, PatchDetailView, DeleteDetailView, APIView
):
    def get(self, request: Request, pk: int) -> Response:
        return super().retrieve(request, pk)

    def patch(self, request: Request, pk: int) -> Response:
        return super().update(request, pk)

    def delete(self, request: Request, pk: int) -> Response:
        return super().destroy(request, pk)
