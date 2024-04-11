# Install me

## pip

``` bash
python3 -m venv packenv
call packenv\scripts\activate.bat

pip3 install -r requirements.txt


python -m pip freeze > requirements.txt
```

Build exe
```
packenv\Scripts\activate.bat

cp packenv\Lib\site-packages\PyQt6 ./

pyinstaller  .\Проверяйка.spec
```
