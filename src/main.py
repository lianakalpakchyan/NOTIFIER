from src.app.views import APIView
from flask import Flask

app = Flask(__name__)

app.add_url_rule('/events/', view_func=APIView.as_view('APIView'))
app.run(debug=True)






