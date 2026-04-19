import os
import shutil
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Restore database from backup'

    def add_arguments(self, parser):
        parser.add_argument(
            'backup_file',
            type=str,
            help='Backup filename to restore',
        )
        parser.add_argument(
            '--create-backup',
            action='store_true',
            help='Create backup of current database before restoring',
        )

    def handle(self, *args, **options):
        backup_filename = options['backup_file']
        backup_dir = os.path.join(settings.MEDIA_ROOT, 'backups')
        backup_path = os.path.join(backup_dir, backup_filename)
        db_path = settings.DATABASES['default']['NAME']
        
        if not os.path.exists(backup_path):
            self.stdout.write(
                self.style.ERROR(f'Backup file not found: {backup_filename}')
            )
            return
        
        if options['create_backup']:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
            emergency_backup = f'emergency_backup_{timestamp}.sqlite3'
            emergency_path = os.path.join(backup_dir, emergency_backup)
            shutil.copy2(db_path, emergency_path)
            self.stdout.write(
                self.style.SUCCESS(f'Emergency backup created: {emergency_backup}')
            )
        
        try:
            shutil.copy2(backup_path, db_path)
            self.stdout.write(
                self.style.SUCCESS(f'Database restored from: {backup_filename}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Restore failed: {str(e)}')
            )
