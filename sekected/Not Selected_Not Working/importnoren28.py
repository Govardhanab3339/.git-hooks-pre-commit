import zipfile
 
with zipfile.ZipFile("NorenRestApi-0.0.28-py2.py3-none-any.whl") as f:
    f.extractall('.')