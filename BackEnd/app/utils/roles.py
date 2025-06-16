def is_admin(user): return user.get("role") == "administrator"
def is_user(user): return user.get("role") == "user"
def is_technician(user): return user.get("role") == "technician"
