# SE_Project
 
## Developing Instructions:
> [!NOTE]
> Read more about Virtual Environment here:
> https://realpython.com/python-virtual-environments-a-primer/
> This is just a summary.

1. Create a new Python Virtual Environment:
```batch
python.exe -m venv venv
```

2. Activate the Virtual Environment:
```batch
.\venv\Scripts\activate
```

3. Install the packages:
```batch
pip install -r requirements.txt
```

4. Start the Flask server:
```batch
python app.py
```

Or:
```batch
flask run
```

## Installing Packages:
Installing packages is just like normal:
```batch
pip install package_name
```

Packages installed in the Virtual Environment will stay in that environment.
## Deactivating:
Run
```
deactivate
```
and you will not be using that environment anymore.