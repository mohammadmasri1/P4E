import logging
from flask import Flask, request, render_template, abort, flash
from config import Config
from utils.ip_validator import check_ip_access

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format=Config.LOG_FORMAT
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('error.html',
                         error_code=403,
                         error_title='Forbidden Access',
                         error_message='You are not authorized to access this resource.'), 403

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html',
                         error_code=404,
                         error_title='Page Not Found',
                         error_message='The requested page could not be found.'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html',
                         error_code=500,
                         error_title='Internal Server Error',
                         error_message='An unexpected error has occurred.'), 500

@app.route("/")
def index():
    # Get real IP behind proxies
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ',' in user_ip:  # Get the first IP if multiple are present
        user_ip = user_ip.split(',')[0].strip()
    
    logger.info(f"Access attempt from IP: {user_ip}")
    
    if check_ip_access(user_ip, Config.ALLOWED_IPS):
        return render_template('form.html', form_url=Config.MICROSOFT_FORM_URL)
    else:
        logger.warning(f"Unauthorized access attempt from IP: {user_ip}")
        return abort(403)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
