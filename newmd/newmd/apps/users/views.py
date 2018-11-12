import random

# Create your views here.
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView

from newmd.libs.yuntongxun.sms import CCP


class SMSCodeView(APIView):
    """发送短信验证码"""

    def get(self, request, mobile):
        # 获取redis连接
        redis_conn = get_redis_connection('verify_codes')

        # 60秒内不重发短信
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return Response({"message": "发送短信过于频繁"})

        # 生成和发送短信验证码
        sms_code = '%06d' % random.randint(0, 999999)
        ccp = CCP()
        ccp.send_template_sms(mobile, [sms_code, '1'], 1)
        print(sms_code)
        # 返回结果
        return Response({'message': 'ok'})

