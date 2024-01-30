from rest_framework import serializers
import csv

class CSVFileValidator:
    def __call__(self, file):
        if not file.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed.")
        try:
            dialect = csv.Sniffer().sniff(file.read(1024).decode('utf-8'))
            file.seek(0)
        except csv.Error:
            raise serializers.ValidationError("Invalid CSV file.")