from app import app
import webbrowser

if __name__ == '__main__':
    # opens the web browser
    webbrowser.open('http://localhost:5000', new=2, autoraise=True )
    # runs the app
    app.run()