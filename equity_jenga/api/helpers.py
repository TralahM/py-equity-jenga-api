from datetime import datetime, timedelta


def todaystr():
    return datetime.today().date().strftime("%Y-%m-%d")


def token_expired(last_auth):
    if datetime.now() - last_auth > timedelta(seconds=3000):
        return True
    else:
        return False


def timenow():
    return datetime.now()


# print(todaystr())
