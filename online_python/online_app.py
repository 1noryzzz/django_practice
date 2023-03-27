import subprocess
from pathlib import Path
from django.conf import settings
from django.http import HttpResponse
from django.urls import re_path

from django.views.decorators.http import require_POST  # 目前的 API 视图只能用于接收 POST 请求
from django.views.decorators.csrf import csrf_exempt  # 禁用csrf
from django.http import JsonResponse  # 用于返回 JSON 数据

BASE_DIR = Path(__file__).resolve().parent


setting = {
    "DEBUG": True,
    "ROOT_URLCONF": __name__,
    "SECRET_KEY": "django-insecure-$oew@_y_vhw9n3!=@n8%ptl)ee#s1@t6r!w8ar$_t55+xs6k(t",
}

settings.configure(**setting)


def run_code(code):
    """
    subprocess.check_output:

    By default, all communication is in bytes, and therefore any "input"
    should be bytes, and the return value will be bytes.  If in text mode,
    any "input" should be a string, and the return value will be a string
    decoded according to locale encoding, or by "encoding" if set. Text mode
    is triggered by setting any of text, encoding, errors or universal_newlines.
    """
    try:
        output = subprocess.check_output(
            ["python", "-c", code],
            universal_newlines=True,
            stderr=subprocess.STDOUT,
            timeout=5,
        )
    except subprocess.CalledProcessError as e:
        output = e.output
    except subprocess.TimeoutExpired as e:
        output = "Time Out"
    return output


def home(request):
    # return HttpResponse("Hello world!")
    with open(BASE_DIR / r"index.html", "rb") as f:
        html = f.read()
    return HttpResponse(html)


@csrf_exempt
@require_POST
def api(request):
    print("in api")
    code = request.POST.get("code")
    print(code)
    output = run_code(code)
    print(output)
    return JsonResponse(data={"output": output})


urlpatterns = [
    re_path("^$", home, name="home"),
    re_path("^api/$", api, name="api"),
]

if __name__ == "__main__":
    import sys
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
