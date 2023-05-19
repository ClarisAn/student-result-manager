import os
import logging
from main.main import app

'''Script that binds the Flask App to port 5050'''

if __name__ == '__main__':
    logging.info('Starting Application...')
    port = os.environ.get("PORT", 5050)
    app.run(host='0.0.0.0', port=port, debug=True)
