from src import create_app
import os

def run():
    from waitress import serve
    app = create_app()

    serve(app, host='0.0.0.0', port=os.getenv('PORT', 5555))

if __name__ == "__main__":
    run()