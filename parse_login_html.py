def get_username_id(login_page):
    lines = login_page.split('\n')
    for line in lines:
        if "Gebruikersnaam" in line:
            return line.split("\"")[1]


def get_password_id(login_page):
    lines = login_page.split('\n')
    for line in lines:
        if "Wachtwoord" in line:
            return line.split("\"")[1]


def get_deviceprint_id(login_page):
    lines = login_page.split('\n')
    for line in lines:
        if "add_deviceprint" in line:
            return line.split("\'")[3]
