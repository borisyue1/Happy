from app import app
import os

port = int(os.environ.get("PORT", 5000))
DEBUG = os.environ.get("DEBUG", False)
if not DEBUG:
	app.run(debug=DEBUG, host="0.0.0.0", port=port)
