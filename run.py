from flask import Flask, render_template, request
import getpass
from threading import Thread
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html', message=None)

@app.route('/run_script', methods=['POST'])
def run_script():
   jira_url = request.form['jira_url']
   username = request.form['username']
   api_token = request.form['api_token']

   # Run your script in a separate thread to avoid blocking the web server
   script_thread = Thread(target=run_jira_script, args=(jira_url, username, api_token))
   script_thread.start()

   message = "Script is running. Check your console for progress."
   return render_template('index.html', message=message)

def run_jira_script(jira_url, username, api_token):
   # Replace the following with the path to your script
   script_path = "get-dupe-cfs.py"

   # Run the script using subprocess
   subprocess.run(['python3', script_path, jira_url, username, api_token])

   # After the script completes, update the message
   message_final = "Script completed. Check the console for the final status."
   app.logger.info(message_final)
   with app.app_context():
       return render_template('index.html', message_final=message_final)

if __name__ == '__main__':
   app.run(debug=True)
