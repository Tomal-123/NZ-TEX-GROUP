import os
import shutil
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Create database backup'

    def add_arguments(self, parser):
        parser.add_argument(
            '--auto',
            action='store_true',
            help='Run automatically (for scheduled backups)',
        )
        parser.add_argument(
            '--keep',
            type=int,
            default=7,
            help='Number of backups to keep (default: 7)',
        )

    def handle(self, *args, **options):
        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        db_path = settings.DATABASES['default']['NAME']
        backup_dir = os.path.join(settings.MEDIA_ROOT, 'backups')
        
        os.makedirs(backup_dir, exist_ok=True)
        
        backup_filename = f'nztex_backup_{timestamp}.sqlite3'
        backup_path = os.path.join(backup_dir, backup_filename)
        
        try:
            shutil.copy2(db_path, backup_path)
            self.stdout.write(
                self.style.SUCCESS(f'Backup created: {backup_filename}')
            )
            
            self.clean_old_backups(backup_dir, options['keep'])
            
            if options['auto']:
                self.stdout.write(
                    self.style.SUCCESS('Auto backup completed')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Backup failed: {str(e)}')
            )

    def clean_old_backups(self, backup_dir, keep_count):
        try:
            backups = sorted([
                f for f in os.listdir(backup_dir) 
                if f.startswith('nztex_backup_') and f.endswith('.sqlite3')
            ], reverse=True)
            
            for old_backup in backups[keep_count:]:
                old_path = os.path.join(backup_dir, old_backup)
                os.remove(old_path)
                self.stdout.write(
                    self.style.WARNING(f'Deleted old backup: {old_backup}')
                )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Could not clean old backups: {str(e)}')
            )
