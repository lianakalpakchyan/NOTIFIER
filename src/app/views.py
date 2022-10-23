from flask import Flask, request, Response
from flask.views import MethodView
from src.infrastructure.controllers import APIController

app = Flask(__name__)


class APIView(MethodView):
    def post(self):
        try:
            request_data = request.get_json()
            api_controller = APIController()
            server_response = api_controller.process_event(request_data)
            if server_response != 'not send':
                return Response(server_response, status=200)
            else:
                return Response(server_response, status=500)
        except Exception as e:
            return Response(str(e), status=500)
