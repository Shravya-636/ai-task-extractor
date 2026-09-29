from app.database import engine

try:
    with engine.connect() as connection:
        print("DATABASE CONNECTION SUCCESSFUL")
except Exception as error:
    print("DATABASE CONNECTION FAILED")
    print(error)