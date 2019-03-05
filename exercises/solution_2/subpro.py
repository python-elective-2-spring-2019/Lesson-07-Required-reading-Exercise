import subprocess
import os

def clone_all_repos(repo_url_list):
    for repo_clone_url in repo_url_list:
        # clone the repositories from the list of urls
        msg = subprocess.run(['git', 'clone', repo_clone_url])
        
        # print(msg) # for logging
        # if the returncode of the subprocess is 128, the the repo alredy exits and is therefor already cloned.
        # if that case we should pull to make sure to have the newest version of the repo.
        if msg.returncode != 0:
            # split the clone url at the '/' so you will have ex: ['https:', 'github.com', 'python-elective-development'] etc.
            repo_name_list = repo_clone_url.split('/')
            # get the last element in the list e.g. : 'day1_intro.git'. this is the repository name
            repo_name_string = repo_name_list[-1]
            # remove the .git extensinon from the repo_name
            repo_name = repo_name_string[0:-4]
            # get the current directory like: pwd in terminal
            cwd = os.getcwd()
            # Change directory into the reponame folder. Like 'cd day1_intro' in terminal
            os.chdir(cwd + '/' +  repo_name)
            # print out to log 
            #subprocess.run('pwd')
            # run the git pull command from inside the eg. 'day1_intro' folder
            subprocess.run(['git', 'pull', 'origin', 'master'])
            # change the directory back to its parrent. like 'cd ..'
            os.chdir('..')

        # print(msg) # for logging

    # print out a list of directories just cloned or updated
    # 'ls' is also an option instead of 'tree'
    print(subprocess.call(["tree", "-L", "2", "-a"]))

def push_to_github():
    pass


