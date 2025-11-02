import datetime
import jwt
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.conf import settings

# Nota: para demo usamos SECRET_KEY de Django. En producción usa una clave distinta para JWT.
SECRET = settings.SECRET_KEY

@csrf_exempt
@require_POST
def jwt_issue(request):
    """
    Emite un token JWT al recibir credenciales válidas por POST (x-www-form-urlencoded).
    Campos:
      - username
      - password
    """
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)
    if not user:
        return JsonResponse({'error': 'Credenciales inválidas'}, status=401)

    # sub debe ser string según el estándar JWT y PyJWT >= 2
    payload = {
        'sub': str(user.id),
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow(),
    }

    token = jwt.encode(payload, SECRET, algorithm='HS256')
    return JsonResponse({
        'access': token,
        'message': 'Token emitido correctamente',
        'expires_in': '1 hora'
    })

def jwt_protected(request):
    """
    Ruta protegida por JWT. Enviar header:
      Authorization: Bearer <token>
    """
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return HttpResponseForbidden('Falta el token o formato incorrecto')

    # Extraer token de forma segura y eliminar espacios accidentales
    token = auth_header.split(' ', 1)[1].strip()

    try:
        decoded = jwt.decode(token, SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse({'error': 'Token expirado'}, status=401)
    except jwt.InvalidTokenError as e:
        # Devolvemos el detalle para diagnóstico (útil en entorno de desarrollo)
        return JsonResponse({'error': 'Token no válido', 'detail': str(e)}, status=401)

    return JsonResponse({
        'ok': True,
        'user_id': int(decoded['sub']),  # opcional: convertir de vuelta a int
        'username': decoded['username']
    })