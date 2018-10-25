# Country Specific Music Analyzer
App: https://country-music-analyzer.herokuapp.com/

# Running the app locally

Dependencies are managed with a `virtualenv`. Trigger the virtualenv by running `source venv/bin/activate` in the repository root. Now you can start the app by running `python app.py`, and it should we visible with your web browser in `http:127.0.0.1:8050/`.

# Managing dependencies

Dependencies are managed in `requirements.txt` file. When addind new Python libraries to the project, run `pip freeze > requirements.txt` in the `virtualenv` in order to update the requiremnts.txt` to match the libraries used in Python source files.
