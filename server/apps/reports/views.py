import pandas as pd

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.tables.models import Table


@login_required
def report(request):
    if request.method == 'GET':
        file = Table.objects.get(user=request.user).data_table
        if not file:
            messages.error(request, 'Вы не можете создать отчёт без таблицы.')
            return redirect('main_page')

        df = pd.read_csv(file)[:30]
        data = {
            'table': df.to_html(),
            'columns': df.columns,
        }

    if request.method == 'POST':
        # Если кто то это читает, то сорри за говнокод ниже, я был уставший.
        # Здесь, параметры фильтрации которые задаёт юзер на странице /report/
        # превращаются в строковое условие для pandas.DataFrame.

        file = Table.objects.get(user=request.user).data_table
        df = pd.read_csv(file)
        conditions = []
        for column in df.columns:
            if column in request.POST:
                col_value = repr(request.POST[column]) if not request.POST[column].isdigit() else request.POST[column]
                raw_cond = request.POST['choice_'+column]
                if raw_cond == 'Больше':
                    cond = '>'
                elif raw_cond == 'Равно':
                    cond = '=='
                else:
                    cond = '<'
                if column and cond and col_value != "''":
                    conditions.append((column, cond, col_value))

        # Retrieve empty table if without conditions
        if not conditions:
            data = {
                'table': df[:0].to_html(),
                'columns': df.columns,
            }
            return render(request, 'reports/report.html', context=data)

        conditions = [f'(df[{repr(cond[0])}]{cond[1]}{cond[2]})' for cond in conditions]
        condition = ''
        for i, cond in enumerate(conditions):
            condition += cond
            if i != len(conditions)-1:
                condition += ' & '
        data = {
            'table': eval('df['+condition+']').to_html(),
            'columns': df.columns
        }
    return render(request, 'reports/report.html', context=data)
