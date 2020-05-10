#!/bin/sh
pwd
ls -l
gunicorn -k eventlet -w 1 app:app --bind=0.0.0.0:8003
