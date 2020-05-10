#!/bin/sh

gunicorn --chdir app -k eventlet -w 1 app:app --bind=0.0.0.0:8003
