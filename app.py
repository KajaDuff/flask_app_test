import os

from app import create_app

#config_name = os.getenv('FLASK_CONFIG')
app = create_app()
#serve(app, host="0.0.0.0", port="70700")

if __name__ == '__main__':
    app.run()

#if __name__ == "__main__":
#    app.run(host='0.0.0.0', port=80800)