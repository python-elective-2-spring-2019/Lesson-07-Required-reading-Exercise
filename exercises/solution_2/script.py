from urllib.request import urlopen

# get a list of all repos in the organization and save it to a string
response = urlopen('https://api.github.com/orgs/python-elective-development/repos?per_page=100')
js = response.read().decode('utf-8')

# split the string into a list whenever the 'clone_url' word appears
response_list = js.split('clone_url')

# create a list for holding the clone urls
real_list = []

# loop through the respone_list
i = 1
while i < len(response_list):

    # same each element in a string
    temp = response_list[i]
    # slice the string so the ":" is cut away
    temp = temp[3:]
    # split the string at the first " (the end of the clone_url)
    # this will leave us with only the clone_url itself at a lists 0 postion 
    # and the rest in the comming positions
    temp_list = temp.split('"')

    # we only need the info at the lists 0 position, so append this to the real_list
    real_list.append(temp_list[0])
    i = i+1


# print(real_list)





