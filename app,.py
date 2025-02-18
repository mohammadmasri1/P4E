from flask import Flask, request, abort, render_template

app = Flask(__name__)

# List of allowed IP addresses (replace with your lab's IP range)
allowed_ips = ['192.168.201.188', '192.168.137.1', '127.0.0.1', '10.154.35.110']

@app.before_request
def limit_remote_addr():
    if request.remote_addr not in allowed_ips:
        abort(403)  # Forbidden

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
