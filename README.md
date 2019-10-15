# OMSv1

# install pyodbc
    RedHat Enterprise Server 7 - for centos 7
    #https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15

# run production
    export FLASK_APP=run.py
    export FLASK_ENV=production
    gunicorn -c .api/configs/gunicorn.config.py wsgi:app