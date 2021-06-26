from werkzeug.contrib.profiler import ProfilerMiddleware

from api import app

app.wsgi_app = ProfilerMiddleware(app.wsgi_app,restrictions=[100])
app.run(debug=True)