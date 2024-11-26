from app import create_app
import sys

app = create_app()

if __name__ == '__main__':
    no_reload = '--no-reload' in sys.argv
    app.run(
        host='127.0.0.1',
        port=8080,
        debug=True,
        use_reloader=not no_reload
    )
