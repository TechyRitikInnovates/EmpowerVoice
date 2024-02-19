import multiprocessing
import subprocess

def run_script(script):
    subprocess.call(['python', script])

if __name__ == '__main__':
    # scripts = ['drive.py', 'telebot.py', 'live.py', 'ngrok.py']
    scripts = ['live.py', 'ngrok.py']
    with multiprocessing.Pool(processes=len(scripts)) as pool:
        pool.map(run_script, scripts)
