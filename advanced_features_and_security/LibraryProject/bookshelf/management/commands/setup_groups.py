from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

class Command(BaseCommand):
    help = 'Setup groups and permissions for bookshelf app'

    def handle(self, *args, **options):
        # Define groups and their permissions
        groups_permissions = {
            'Viewers': ['can_view'],
            'Editors': ['can_view', 'can_create', 'can_edit'],
            'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete'],
        }

        content_type = ContentType.objects.get_for_model(Book)

        for group_name, perms in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            for perm_codename in perms:
                permission = Permission.objects.get(codename=perm_codename, content_type=content_type)
                group.permissions.add(permission)
            self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" set up with permissions: {perms}'))
