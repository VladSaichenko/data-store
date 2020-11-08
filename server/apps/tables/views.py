import pandas as pd

from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.tables.models import Table


@login_required
def main_page(request):
    if request.method == 'GET':
        table = Table.objects.get(user=request.user)
        file = table.data_table

        if file:
            try:
                df = pd.read_csv(file)
            except UnicodeDecodeError:
                table.data_table = None
                table.save()
                messages.error(request, 'Таблица закодирована в неверном формате.')
                return redirect('main_page')

            data = {
                'table': df.to_html(),
                'columns': df. columns,
                'table_info': {
                    'columns_len': len(df.columns),
                    'table_len': len(df),
                }
            }
        else:
            data = {
                'table': None
            }
    return render(request, 'tables/main_page.html', context=data)


@login_required
def upload_csv(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            messages.error(request, 'Вы не отправили файл.')
            return redirect('main_page')

        if not request.FILES['file'].name.endswith('.csv'):
            messages.error(request, 'Отправляемый файл не является .csv')
            return redirect('main_page')

        table = Table.objects.get(user=request.user)
        table.data_table = request.FILES['file']
        table.save()
        return redirect(reverse('main_page'))
    return HttpResponse(status=403)


@login_required
def append_to_csv(request):
    if request.method == 'POST':
        table = Table.objects.get(user=request.user)
        file = table.data_table
        df = pd.read_csv(file.path)
        row = {column: request.POST[column] for column in df.columns}
        df = df.append(row, ignore_index=True)
        df.to_csv(file.path, index=False)

        return redirect('main_page')
    return HttpResponse(status=403)


@login_required
def add_column(request):
    if request.method == 'POST':
        table = Table.objects.get(user=request.user)
        df = pd.read_csv(table.data_table)
        df[request.POST['new_column']] = ''
        df.to_csv(table.data_table.path, index=False)
        return redirect('main_page')
    return HttpResponse(status=403)
