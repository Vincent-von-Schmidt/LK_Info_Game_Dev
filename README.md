## install & build

### with python installed

#### Windows
```` python
python -m pip install -r requirements.txt
python src/main.py
````

#### Unix bassed
````python
python3 -m pip install -r requirements.txt
python3 src/main.py
````

## without python installed -> WIP
Docker is required for use without python. 
````bash
sudo docker build py_app
sudo docker run -it --rm py_app
````
