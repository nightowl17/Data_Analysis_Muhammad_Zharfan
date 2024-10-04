# Running the Dashboard on streamlit

## 1. Setup Environment - Anaconda
```
conda create --name main-ds python=3.12.7
conda activate main-ds
pip install -r requirements.txt
```

## 2. create new directory and finish setting up the environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```
## Run the steamlit app (dashboard.py)
After i create dashboard.py as the name of my dashboard app and the app has been built
this is how to run the app:
1. open up terminal (you can do it in visual studio code for example)
2. type : 
```
streamlit run dashboard.py
```
3. visual studio code will open on a new browser tab(chrome) showing the dashboard.py streamlit app
4. or you can run them by opening link below in a browser (streamlit cloud link to the app):
   https://finalprojectdataanalysismuhammadzharfan-kukgwkjfcmh4mlszysbdct.streamlit.app/
