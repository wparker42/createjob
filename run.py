import os
from cjapp import app

env_name = "Testing"

while env_name is not "Testing":
    port = int(os.environ.get("PORT", 8090))
    debug = True if os.environ.get("DEBUG_MODE") == 'True' else False
    app.run(host="0.0.0.0", port=port, debug=debug)
    break
else:
    app.run(host="0.0.0.0", port=5000, debug=True)