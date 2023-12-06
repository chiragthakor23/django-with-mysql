from django.db import connection
from django.shortcuts import render
import csv
from django.http import HttpResponse


def show_databases(request):
    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES")
    databases = [db[0] for db in cursor.fetchall()]
    return render(request, 'databases.html', {'databases': databases})


def show_tables(request):
    selected_database = request.GET.get('selected_database')
    selected_table = request.GET.get('selected_table')
    
    if selected_database:
        cursor = connection.cursor()
        cursor.execute(f"USE {selected_database}")
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        if selected_table:
            cursor.execute(f"SELECT * FROM {selected_table}")
            table_data = cursor.fetchall()  # Fetch data from the selected table
            columns = [col[0] for col in cursor.description]  # Fetch column names
            
            # Generate CSV content
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{selected_table}.csv"'
            
            writer = csv.writer(response)
            writer.writerow(columns)  # Write column headers
            writer.writerows(table_data)  # Write table data rows
            
            return response

        return render(request, 'tables.html', {
            'tables': tables,
            'selected_database': selected_database,
            'selected_table': selected_table,
            'error_message': 'Please select a table'
        })
    else:
        return render(request, 'databases.html', {'error_message': 'Please select a database'})

