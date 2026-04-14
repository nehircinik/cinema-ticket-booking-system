from database import create_tables
from auth import register_user

create_tables()

try:
    register_user("Admin", "admin@mail.com", "admin123", "admin")
except:
    pass

print("Database ready. Use gui.py")