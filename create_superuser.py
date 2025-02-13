import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.myproject.settings")
django.setup()

from myapp.models import ABUser
from django.contrib.auth.models import Group, Permission

def create_admin_user():
    if not ABUser.objects.filter(username="admin").exists():
        ABUser.objects.create_superuser("admin", "miller.jshaw@gmail.com", "root")
        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")

def create_user_group():
    group_name = "user"
    group, created = Group.objects.get_or_create(name=group_name)

    if created:
        print(f"Group '{group_name}' created.")
    else:
        print(f"Group '{group_name}' already exists.")

    permissions = Permission.objects.filter(codename__in=["view_abuser", "change_abuser"])
    group.permissions.set(permissions)

if __name__ == "__main__":
    create_admin_user()
    create_user_group()
