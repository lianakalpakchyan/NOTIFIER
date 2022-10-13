import os
from flask import Flask, request, Response
from flask.views import MethodView
from src.infrastructure.controllers import APIController

app = Flask(__name__)


class APIView(MethodView):
    @staticmethod
    @app.route('/')
    def hello_world():
        return 'Hello world'

    @staticmethod
    @app.route('/events/', methods=['POST'])
    def post():
        try:
            request_data = request.get_json()
            api_controller = APIController()
            api_controller.process_event(request_data)
            log_path = os.path.join('..', 'logs', 'notifier.log')
            with open(log_path) as app_logs:
                server_response = app_logs.readlines()[-1]
                status = 500
                if 'successfully' in server_response:
                    server_response = 'The task is successfully done!'
                    status = 200
                else:
                    server_response = server_response.split('::')[-1]
            return Response(server_response, status=status)
        except Exception as e:
            return Response(str(e), status=500)


def main():
    app.add_url_rule('/', view_func=APIView.as_view('APIView'))
    app.run(debug=True)


if __name__ == '__main__':
    main()

