# Rotation Schedular (MOCK)

This Schedular is to help generate a schedule 
of rotations for med students per the corresponding year.

## Requirements to run locally 
- Python 3.3 or higher 
- IDE (preferably PyCharm, but any python interpreter will work)
- MySQL workbench
- Access to the Internet (initially)

# Setup 
1) clone the repo by running this command

```bash
git clone <url-to-github-repo>
```

2) open repository root and install a virtual environment and run that env by running the commands:
   ### Mac: 
    ```bash
    python3 -m venv venv
   
   . venv/bin/activate
    ```
   
    ### Windows:
    ```bash
    c:\>c:\Python35\python -m venv c:\path\to\myenv
   
    c:\> venv\Scripts\activate.bat 
    ```
    **note**: the first part is the path to the location of where you have python installed. 
    For more clarity, please visit [here](https://docs.python.org/3/library/venv.html).

  

3) Create and store Enviroment variables
   1) Right-Click root folder 'mock-schedular' and click new file
   2) name file '.env' with no preceding name. just '.env'
   3) in that file give write the following variables and 
   give values to your local instance of you Data base 
   ```bash
    FLASK_ENV=development
    FLASK_APP=schedular/server/main.py
    SCHEDULAR_DB_HOST=127.0.0.1
    SCHEDULAR_DB_USER=root
    SCHEDULAR_DB_PASS=password
    SCHEDULAR_DB_NAME=schedular
    ```

4) Ready to run 
   
  
    






