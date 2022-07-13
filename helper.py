def find_int(findInt):

    string_id = ""
    int_id = -1

    for string in findInt:
        for eachChar in string:
            if eachChar.isdigit():
                string_id += eachChar

    if string_id == "":
        pass
    else:
        int_id = int_id + int(string_id) + 1
    return int_id


def find_username_email(data):
    getData = str(data).replace('"', "").split()
    email = ""
    username = ""

    i = 0
    while i < len(getData):

        if getData[i] == "email:":
            # this is email information
            email += getData[i + 1].replace(",", "")

        elif getData[i] == "username:":
            # this is username information
            username += getData[i + 1]

        i += 1

    return [email, username]
