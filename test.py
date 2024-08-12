import users


def auth_users(*args, **kwargs):
    for i in users.views.auth_users:
        print(i)