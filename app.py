import logging
from main.main import app

'''Script that binds the Flask App to port 5050'''

if __name__ == '__main__':
    logging.info('Starting Application...')
    app.run(host='0.0.0.0', port=5050, debug=True)
