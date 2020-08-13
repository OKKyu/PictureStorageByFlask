# Name
  PictureStorage

# overwiev
  This project is used to store image file into mobile. 
  

# Requirement
  python3, python3-venv (>=3.5)  

# Download
  please copy your preference directory.  

# setup
 please run setup.sh  
 first,  virtual environment is maked in "PictureStorage/venv/"
 second, updating pip in virtual environment.
 third,  dependency library is imported by pip with requirements.txt

# run
 please type shell below.
   run run.sh  worker-num  hostname(ip address) portnum
 
 This shell use gunicorn with WSGI.
 if you want to use other WSGI, you can overwirte this shell source.
 
# Usage
  This project is only WebAPI. It is haven't front end GUI.

# Structure

- `PictureStorage/main.py` Flask app (entry point)  
- `PictureStorage/env/`        config files and certificate files.
- `PictureStorage/data/`       Sended Picture files is storaged in this directory.  
- `PictureStorage/venv/`       vurtualenv folder. This directory is generated automatic by setup.sh
- `PictureStorage/README.md`   explanation about Web application that implementated by this project  
- `PictureStorage/run.sh`      execute this web application on WSGI (gunicorn)
- `PictureStorage/setup.sh`    setup about this web application   

# Lisense
   please writing below about license.  
   for example  
   
   PictureStorage version 1.0.0  
   (c) 2020 OKKyu allrights reserved under MIT license.  
   
## Author
OKKyu
