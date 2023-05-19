from flask import Flask
from flask_cors import CORS
import router
from config import config
import db

def create_app():
  # Generate Flask App Instance
  app = Flask(__name__)

  # Read DB setting & Initialize
  app.config.from_object(config.Config)
  db.init_db(app)
  db.init_ma(app)

  # Register Router Instance
  app.register_blueprint(router.router)

  # Additional Configuration 
  app.config['JSON_AS_ASCII'] = False #日本語文字化け対策
  app.config["JSON_SORT_KEYS"] = False #ソートをそのまま
  CORS(
    app,
    resources = {
      r"/api/*": {"origins": ["http://localhost", "http://localhost:4200"]}
    }
  )
  return app

app = create_app()
if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True, port=5000, threaded=True, use_reloader=False)