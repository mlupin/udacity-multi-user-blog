from handlers.blog import BlogHandler
from helpers import valid_username
from helpers import valid_password
from helpers import valid_email
from models.user import User


class Signup(BlogHandler):
    def get(self):
        self.render("signup-form.html")

    def post(self):
        """
        Checks if inputs are valid.
        """
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username=self.username,
                      email=self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

    def done(self):
        """
        Checks if user already exists
        """
        u = User.by_name(self.username)
        if u:
            error = 'That user already exists.'
            self.render('signup-form.html', error_username=error)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()
            self.login(u)
            return self.redirect('/blog')
