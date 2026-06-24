# Crappy Expense Tracker — 沒什麼功能的記帳程式

軟體庫：
* `QT6`
* `PySide6`
* `Kirigami` (KDE 的 QT 模版)
* `appsdir` (資料夾位置)

可能只能在 Linux 上用……

安裝：
```bash
$ python -m venv --system-site-packages env/
$ source env/bin/activate
$ python -m pip install .
```

把寵物程式資料夾放在 `src/PetLedger`。建議在命令列開程式，才能知道錯在哪。

執行：
```bash
$ source env/bin/activate
$ expensetracker
```

要在 User Config Dir 內放入 `settings.json`:
```json
{
        "data_dir": "<資料路經，如：/home/yichm/Sync/budget>"
}
```

紀錄以純文字存檔，名字為 `<月>_<日>.tsv`，標籤存在 `tags.txt` 內，用空白字元分隔。
