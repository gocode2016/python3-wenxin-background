import hashlib, base64
import random, string

class UserService(object):
    @staticmethod
    def cookieAuth(user_info):
        m = hashlib.md5()
        str = "%s-%s-%s-%s" % (user_info.uid, user_info.login_name, user_info.login_pwd, user_info.login_salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def genpwd(pwd, salt):
        m = hashlib.md5()
        str = "%s-%s" % (base64.encodebytes(pwd.encode("utf-8")), salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def genpwdsalt():
        salt = [random.choice((string.ascii_letters + string.digits)) for i in range(16)]
        return ''.join(salt)
