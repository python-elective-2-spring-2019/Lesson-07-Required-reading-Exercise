import glob
import os


def create_curriculum_list():

    # Get a list of uris for the readme.md files
    # in this directories and its subdirecttories
    # e.g: ['readme.md', 'unit_test/readme.md', 'day1_intro/readme.md']
    file_uri_list = get_file_uri_list()
    # print(files)

    # list containing all text from each readme file as one element
    files_content_list = get_files_content_list(file_uri_list)
    # print(files_content_list)

    # List containing curriculum lists from each readme file in one element
    temp_list = get_list_containing_curriculum(files_content_list)
    # print(temp_list)

    # remove the first element from each list and merge it into one list
    curriculum_list = remove_first_element_from_lists_and_merge(temp_list)
    # print(curriculum_list)

    # if a string contains more than one bullit point, split it into 2 etc.
    curriculum_list = slice_string_into_smaller_units(curriculum_list)
    # print(curriculum_list)

    # strip each element from /n
    curriculum_list = beautify_list(curriculum_list)
    # print(curriculum_list)

    # Capitalize first letter
    curriculum_list = capitalize_first_letter(curriculum_list)

    # Delete duplicates
    curriculum_set = set(curriculum_list)

    # create a sorted set
    curriculum_set = sorted(curriculum_set)
    print(curriculum_set)

    # write list to file
    write_curriculum_to_md_file(curriculum_set)


def write_curriculum_to_md_file(curriculum_list):
    # get the current directory
    cwd = os.getcwd()
    # print(cwd)

    # create a new directory if it does not already exist
    directory = 'curriculum__xff'
    if os.path.isdir(directory):
        pass
    else:
        os.makedirs(directory)

    # change dir into new directory
    os.chdir(directory)

    cwd = os.getcwd()
    # print(cwd)
    # open new writeable file object
    file = open(cwd + '/curriculum.md', 'w')

    # write header to list
    header_text = '# Curriculum\n > Python Elective I Spring 2019\n\n'
    file.write(header_text) 

    # write curriculum_list to file
    for x in curriculum_list:
        file.write(x)


def capitalize_first_letter(list):
    temp_list = []
    for x in list:
        # capitalize the 4th letter in the string (first letter)
        temp_list.append(x[:3] + x[3:].capitalize())

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
    j = 0
    while j < len(list):
        if list[j].count('*') > 1:
            del list[j]
        j = j + 1

    # print(list)
    return list


def get_list_containing_curriculum(loc_files_content_list):

    tmp_lists_out_curriculum = []

    for x in loc_files_content_list:
        if '## Curriculum' in x:
            spl_list = x.split('### ')

            # print(spl_list)

            for y in spl_list:
                if 'Curriculum' in y:
                    tmp_lists_out_curriculum.append(y.split('Curriculum'))
                   # print('============')

    return tmp_lists_out_curriculum


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


def get_file_uri_list():
    # Get a list of uris for the readme.md files
    # in this directories and its subdirecttories
    # e.g: ['readme.md', 'unit_test/readme.md', 'day1_intro/readme.md']
    return glob.glob('**/readme.md', recursive=True)


if __name__ == "__main__":
    # execute only if run as a script
    create_curriculum_list()
