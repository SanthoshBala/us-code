
tar -cf ./static/preamble.tar ./static/preamble.txt
rm ./static/preamble.txt

dev_appserver.py app.yaml
