import pathlib
import csv
import datetime as dt

class ExpenseService:
    def __init__(self, data_dir: pathlib.Path):
        self.data_dir = pathlib.Path(data_dir)
        if not self.data_dir.is_dir():
            raise ValueError(f'{data_dir} is not a directory')

    def _path_for_date(self, date: dt.date):
        return self.data_dir / date.strftime('%Y_%m.tsv')

    def _read_table(self, date: dt.date):
        pth = self._path_for_date(date)
        table = []
        if pth.exists():
            with pth.open('r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f, delimiter='\t')
                table = [{
                    'date': dt.date.strptime(row[0], "%Y-%m-%d"),
                    'id': int(row[1]),
                    'expense': int(row[2]),
                    'title': row[3],
                    'tags': [s.strip() for s in row[4].split(' ') if s.strip()] if len(row) >= 5 else []
                    } for row in reader if len(row) >= 4]
        return table

    def _write_table(self, date: dt.date, table):
        pth = self._path_for_date(date)
        if pth.exists():
            with pth.open('w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, delimiter='\t')
                for row in table:
                    writer.writerow([
                        dt.date.strftime(row['date'], "%Y-%m-%d"),
                        row['id'],
                        row['expense'],
                        row['title'],
                        " ".join(row['tags'])])

    def write(self, ent: dict):
        table = self._read_table(ent['date'])
        table.append(ent)
        table.sort(key=lambda x: (x['date'], x['id']))
        self._write_table(ent['date'], table)

    def delete(self, date: dt.datetime, seq: int):
        table = self._read_table(date)
        table = [row for row in table if not (row['date'] == date and row['id'] == seq)]
        self._write_table(date, table)

    def update(self, ent: dict):
        table = self._read_table(ent['date'])
        table = [row for row in table if not (row['date'] == ent['date'] and row['id'] == ent['id'])]
        table.append(ent)
        table.sort(key=lambda x: (x['date'], x['id']))
        self._write_table(ent['date'], table)

    def read(self, start: dt.date, end: dt.date):
        if end <= start:
            raise ValueError("End date < start date")
        dates = []
        cmonth, cyear = start.month, start.year
        while cyear != end.year or cmonth != end.month:
            dates.append(dt.date(cyear, cmonth, 1))
            cmonth += 1
            if cmonth > 12:
                cyear += 1

        dates.append(dt.date(cyear, cmonth, 1))
        result = []
        for d in dates:
            try:
                result.extend(self._read_table(d))
            except FileNotFoundError:
                pass
        result = [row for row in result if start <= row['date'] <= end]
        return result
