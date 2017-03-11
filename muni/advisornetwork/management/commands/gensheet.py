from django.core.management.base import BaseCommand, CommandError
from advisornetwork.models import School, Delegate
import csv


class Command(BaseCommand):
    help = 'Generate delegate roster spreadsheet'
    # MUNI XXII, School Name, Position, Committee, Personal Name

    def handle(self, *args, **options):
        rows = []
        s = sorted(School.objects.all(), key=lambda s: s.name)
        for school in s:
            d = sorted(school.delegates.all(), key=lambda d: d.name)
            for delegate in d:
                row = ['Muni XXII', school.name, delegate.position, delegate.committee, delegate.name]
                rows.append(row)

        with open('delegatesheet.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)

        print('Done')