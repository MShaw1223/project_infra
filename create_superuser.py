import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from myapp.models import ABUser
from django.contrib.auth.models import Group, Permission

def create_admin_user():
    print("Checking admin exists...")
    if not ABUser.objects.filter(username="admin").exists():
        ABUser.objects.create_superuser("admin", "miller.jshaw@gmail.com", "root")
        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")

def create_user_group():
    print("Checking if user group exists...")
    group_name = "user"
    group, created = Group.objects.get_or_create(name=group_name)

    if created:
        print(f"Group '{group_name}' created.")
    else:
        print(f"Group '{group_name}' already exists.")

    permissions = Permission.objects.filter(codename__in=[
        "add_abuser", "change_abuser", "delete_abuser", "view_abuser",
        "add_contact", "change_contact", "delete_contact", "view_contact",
        "add_tag"
    ])
    
    print(f"Permissions found: {permissions}")
    group.permissions.set(permissions)
    print("Permissions set.")


create_admin_user()
create_user_group()
