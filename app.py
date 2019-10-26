from app.database import build_schema
from app import app

if __name__ == '__main__':
    #build_schema()
    app.run(debug=True)
