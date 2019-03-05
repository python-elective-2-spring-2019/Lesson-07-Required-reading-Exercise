import glob
import os
import subprocess
from urllib.request import urlopen
import urllib.error
import sys

"""
    STEP-a:
    Ask the user for the url to the organisation or user account on github 
    he or she wants to clone.
    Ask the user for the directory where the clones should be stored
"""


def user_input():

    # IE. https://github.com/python-elective-1-spring-2019/
    # IE. https://github.com/python-elective-2-spring-2019/

    # Ask for URL to github account and Check if the url exists
    while True:
        try:
            apiurl = input("Please specify the Github url: ")
            response = urlopen(apiurl)
            break
        except ValueError as err:
            print('Your input is not in the right format: ', err)
            continue
        except OSError as err:
            print('The spcified URL does not exist:', err)
            continue

    # slice the url so we get the org or username
    organisation = apiurl[19:-1]

    # Where to store repos locally
    directory = input(
        'Where du you want the cloned repos to be stored? (full path): ')
    # add the orgname to the full path
    directory = directory + '/' + organisation
    # print(os.getcwd())

    if os.path.isdir(directory):
        # Change directory
        os.chdir(directory)
        print(
            f'The directory: "{os.getcwd()}" already exist and was left untouched')
    else:
        os.makedirs(directory)
        os.chdir(directory)
        print(f'A new directory was created at: {os.getcwd()}')

    return organisation
    # sys.exit(0)


"""
    STEP-1:
    Get all repositories clone urls from the organization 'python-elective-1-spring-2019' 
    and save them in a list, tuple, set or dictionary. 
    For this you should make use of the 'urllib' module, 
    and you can get all info about the repositories at this << api >>.
"""


def repo_json():

    org = user_input()
    # js is a string containing json from the url
    response = urlopen(f'https://api.github.com/orgs/{org}/repos?per_page=100')
    json = response.read().decode('utf-8')

    # print(json)

    # split the string into a list whenever the 'clone_url' word appears
    response_list = json.split('clone_url')
    # remove the first element, the one before the first clone url
    response_list.pop(0)

    # print(response_list[0])
    return response_list


def url_list():
    response_list = repo_json()
    url_list = []

    for repo_info in response_list:
        # remove the ":" from the beginning of the string by slicing
        repo_info = repo_info[3:]
        # split at " resulting in a list where the first element is the url we need
        repo_info = repo_info.split('"')
        # append url til the list
        url_list.append(repo_info[0])

    # print(url_list)
    return url_list


"""
    STEP 2:
    Clone all repos from the organisation. For this you will need the modul: subprocess
    Or if the repository is alredy cloned you should make sure that you have an up to date 
    version of the repository by a pull request. 
    For some of the tasks in this operation you will need the modul: subprocess like 
    before and for some you will need the module: OS
"""


def clone_repos():
    urllist = url_list()
    # get the current directory like: pwd in terminal
    #cwd = os.getcwd()
    # Change directory from here where this script is running to the subfolder where we want all the reppository clones
    #os.chdir(cwd + '/repos')

    for url in urllist:
        # clone the repositories from the list of url
        msg = subprocess.run(['git', 'clone', url])

        # if repo is already cloned, pull for update
        if msg.returncode != 0:
            pull_repo(url)


def pull_repo(url):
    # split the clone url at the '/' so you will have ex: ['https:', 'github.com', 'python-elective-development'] etc.
    repo_urllist = url.split('/')

    # get the last element in the list e.g. : 'day1_intro.git'. this is the repository name
    repo_name = repo_urllist[-1]

    # remove the .git extensinon from the repo_name
    repo_name = repo_name[0:-4]

    # get the current directory like: pwd in terminal
    cwd = os.getcwd()

    # Change directory into the reponame folder. Like 'cd day1_intro' in terminal
    os.chdir(cwd + '/' + repo_name)

    # run the git pull command from inside the eg. 'day1_intro' folder
    subprocess.run(['git', 'pull', 'origin', 'master'])

    # change the directory back to its parrent. like 'cd ..'
    os.chdir('..')


clone_repos()
# sys.exit()

"""
    STEP 3:
    Traverse through all repos locally and 
    get the readme files content in a list ie. 
    (for this you will need the module: glob
"""


def readme_file_list():
    # Get a list of uris for the readme.md files
    # in this directories and its subdirecttories
    # e.g: ['readme.md', 'unit_test/readme.md', 'day1_intro/readme.md']
    return glob.glob('**/readme.md', recursive=True)


def get_files_content_list(file_uri_list):
    # difine list
    files_content_list = []
    # Open each file using the uri list 'file_uri_list', read the content
    # and append it to the files_content list
    for f in file_uri_list:
        # f is a uri string: 'day1_intro/readme.md' etc. file is an object
        file = open(f)
        # print(file)
        # file.read() gets the text from the file and appends it to the
        files_content_list.append(file.read())
        file.close()

    return files_content_list


# print(readme_file_list())
# sys.exit(0)
"""
    STEP 4: 
    Search the content of the list and find the 
    "## Required reading" paragraph and put the content of 
    that paragraph into list.
"""


def list_containing_required_reading_paragraph(loc_files_content_list):

    tmp_lists_out_curriculum = []

    for x in loc_files_content_list:
        if '## Required reading' in x:
            content_list = x.split('## ')

            # print(spl_list)

            for y in content_list:
                if 'Required reading' in y:
                    tmp_lists_out_curriculum.append(
                        y.split('Required reading'))
                   # print('============')

    return tmp_lists_out_curriculum


"""
    STEP 5:
    Write the list to a required_reading.md in a new curriculum repository. 
    (for this operation you will again need the modul: OS)
        * The links in the readme file should be:
            * Ordered Alphabetically
            * Beginning character should be capitalized
            * The list should look good/normal, 
              * e.g no blank bullet points, no whitepsaces in wrong places etc.
            * No dublicate link should occour.
"""


def write_curriculum_to_md_file(curriculum_list):
    # get the current directory
    cwd = os.getcwd()
    # print(cwd)

    # create a new directory if it does not already exist
    directory = 'required_reading'
    if os.path.isdir(directory):
        pass
    else:
        os.makedirs(directory)

    # change dir into the directory
    os.chdir(directory)

    #cwd = os.getcwd()
    # print(cwd)
    # open new writeable file object
    file = open('required_reading.md', 'w')  # cwd + '/curriculum.md', 'w'

    # write headline to list
    headline = '# Required Reading\n > Python Elective I Spring 2019\n\n'  # get this from
    file.write(headline)

    # write curriculum_list to file
    for x in curriculum_list:
        file.write(x)

    file.close()


"""
    Making the elements in list clean and ready to write to file
"""


def capitalize_first_letter(list):
    temp_list = []
    for x in list:
        # capitalize the 4th letter in the string (first letter)
        temp_list.append(x[:3] + x[3:].capitalize())

    return temp_list


def remove_end_hashtag(list):
    temp_list = []
    for x in list:
        if x[-1] == '#':
            temp_list.append(x[:-1])
        else:
            temp_list.append(x)

    return temp_list


def beautify_list(list):
    temp_list = []
    for x in list:
        # remmove first element if it is a '\n'
        # as long as there is an '\n' at position 1
        condition = True
        while condition:
            if x[0] == '\n':
                x = x[1:]
            else:
                condition = False

        # remove last element if it is a '\n'
        # as long as there is an '\n' at last position
        condition = True
        while condition:
            if x[-1] == '\n':
                x = x[:-1]
            else:
                condition = False

        # add '\n' at all last positions
        x = x + '\n'

        temp_list.append(x)

    return temp_list


def remove_first_element_from_lists_and_merge(loc_temp_list):
    temp_list = []
    for x in loc_temp_list:
        i = 0
        while i < len(x):
            if i != 0:
                temp_list.append(x[i])
            i = i+1

    return temp_list


def slice_string_into_smaller_units(list):
    temp_list = []
    for x in list:
        # if a string contains more than one '*' we need to split it,
        # so each '*' has a unique place in the list
        if x.count('*') > 1:
            loop_temp_list = x.split('*')
            # add the splittet list to the temp_list minus the
            # first element which will be garbage from the split ('\n\n')
            temp_list = temp_list + loop_temp_list[1:]

    # append the new elements to the existing list
    i = 1
    while i < len(temp_list):
        list.append('*' + temp_list[i])
        i = i + 1

    # remove the 'old' elements from the list
    # copy the list
    temp_list = []

    for y in list:
        if y.count('*') > 1:
            pass
        else:
            temp_list.append(y)

    return temp_list


# main function for the part of creating a Required_readme.md file
def create_req_reading_file():

    # Step 3

    # Get a list of uris for the readme.md files
    # in this directories and its subdirecttories
    # e.g: ['readme.md', 'unit_test/readme.md', 'day1_intro/readme.md']
    paths = readme_file_list()

    # list containing all text from each readme file as one element
    texts = get_files_content_list(paths)

    # Step 4

    req_readings = list_containing_required_reading_paragraph(texts)

    # print(req_readings)
    # sys.exit()

    # STEP 5:
    # First do some clean up

    # remove the first element from each list and merge it into one list
    req_read_list = remove_first_element_from_lists_and_merge(req_readings)

    #print(req_read_list)
    #sys.exit()

    # if a string contains more than one bullit point, split it into 2 etc.
    req_read_list = slice_string_into_smaller_units(req_read_list)

    # strip posible '#' in the end of each element
    req_read_list = remove_end_hashtag(req_read_list)

    # strip each element from /n ´s
    req_read_list = beautify_list(req_read_list)

    # Capitalize first letter
    req_read_list = capitalize_first_letter(req_read_list)

    #print(req_read_list)
    #sys.exit()

    # Delete duplicates
    req_read_set = set(req_read_list)

    #print(req_read_set)

    # create a sorted set
    req_read_set = sorted(req_read_set)

    # write set to file
    write_curriculum_to_md_file(req_read_set)


# Call main function
create_req_reading_file()

"""
    STEP 6:
    push that repository to your own github account.
"""

def push_to_github():


    if os.path.isdir('.git'):
        pass
    else:
        msg = subprocess.run(['git', 'init'])
        msg = subprocess.run(['git', 'remote', 'add', 'origin', 'https://github.com/clbokea/required_reading.git'])
    
    msg = subprocess.run(['git', 'add', 'required_reading.md'])
    msg = subprocess.run(['git', 'commit', '-m', '"from script"'])
    msg = subprocess.run(['git', 'push', 'origin', 'master'])

push_to_github()