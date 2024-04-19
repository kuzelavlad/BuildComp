from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ApplicationSerializer, Cost_ApplicationSerializer
from rest_framework.parsers import MultiPartParser, JSONParser
from django.core.mail import send_mail
from application.models import Application, ApplicationFile


class ApplicationCreateView(APIView):
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, format=None):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            files = request.FILES.getlist('document')

            validated_data = serializer.validated_data
            if 'document' in validated_data:
                validated_data.pop('document')

            application = Application.objects.create(**validated_data)

            for file in files:
                ApplicationFile.objects.create(application=application, file=file)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO: сделать возможность отправки формы как в админку, так и на определенную почту

# class ApplicationCreateView(APIView):
#     parser_classes = [MultiPartParser, JSONParser]
#
#     def post(self, request, format=None):
#         serializer = ApplicationSerializer(data=request.data)
#         if serializer.is_valid():
#             files = request.FILES.getlist('document')
#
#             validated_data = serializer.validated_data
#             if 'document' in validated_data:
#                 validated_data.pop('document')
#
#             application = Application.objects.create(**validated_data)
#
#             for file in files:
#                 ApplicationFile.objects.create(application=application, file=file)
#
#             # Отправьте уведомление на почту Alfa-Building@yandex.by
#             subject = 'Новая заявка создана'
#             message = f'Новая заявка была создана на вашем сайте.\n\n' \
#                       f'Имя: {application.name}\n' \
#                       f'Телефон: {application.number}\n' \
#                       f'Сообщение: {application.message}\n'
#
#             # Добавьте ссылки на файлы или их имена в сообщение
#             for file in files:
#                 message += f'Прикреплен файл: {file.name}\n'  # или можно использовать file.url, если файлы доступны по URL
#             from_email = 'order@aroma-stroy.by'
#             recipient_list = ['Alfa-Building@yandex.by']  # Почта Alfa-Building@yandex.by
#
#             send_mail(subject, message, from_email, recipient_list=recipient_list, fail_silently=False)
#
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Cost_ApplicationCreateView(APIView):
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, format=None):
        serializer = Cost_ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


