#!/bin/bash
source mkvenv/bin/activate 

gunicorn -b :$PORT app:app & 
python3 update.py &          
python3 -m bot
