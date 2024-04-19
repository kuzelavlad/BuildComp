from rest_framework.response import Response
from rest_framework.decorators import api_view
from personal.models import Personal
from bs4 import BeautifulSoup


def remove_html_tags(text):
    cleaned_text = BeautifulSoup(text, 'html.parser').get_text()
    return cleaned_text


@api_view(['GET'])
def personal_view(requests):
    personal_view_objects = Personal.objects.all()
    clean_data = []

    for p in personal_view_objects:
        cleaned_description = remove_html_tags(p.description)
        split_desc = cleaned_description.split('\n')

        personal_data = {
            'name': p.name,
            'department': p.department,
            'position': p.position,
            'description': split_desc,
            'pers_image': p.pers_image.url,
        }
        clean_data.append(personal_data)

    return Response(clean_data)
