from app import app
from app.database import build_schema

if __name__ == '__main__':
    build_schema()
    app.run(debug=True)
