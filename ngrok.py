from flask import Flask

# Import Ngrok
from pyngrok import ngrok

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, world!'

if __name__ == '__main__':
    # Start Ngrok when the app is run
    ngrok_tunnel = ngrok.connect(5001)
    print('Ngrok URL:', ngrok_tunnel.public_url)

    try:
        # Run the Flask app
        app.run()
    except KeyboardInterrupt:
        # Disconnect Ngrok when the app is stopped
        ngrok.disconnect(ngrok_tunnel.public_url)
