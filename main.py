#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

USER_RE = re.compile(r"^[a-zA-z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")


def valid_username(username):
    return USER_RE.match(username)


def valid_password(password):
    return PASS_RE.match(password)


def valid_email(email):
    return EMAIL_RE.match(email)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        form = """
        <h1>Welcome</h1>
        <a href="/signup">Click here to sign in or sign up</a>
        """
        self.response.write(form)
        return


class WelcomePage(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        content = "<h1>Welcome {0}</h1>".format(username)
        self.response.write(content)
        return


class SignupPage(webapp2.RequestHandler):
    def write_form(self, error1="", error2='', error3="", username="", password="", verify="", email=""):
        form = """
            <h1><a href='/signup'>User Sign-up</a></h1>
                <form action='/signup' method='post'>
                    <label>Username:</label><input type='text' name='username' value='""" + username + """'/>""" + error1 + """<br>
                    <label>Password:</label><input type='password' name='password'/>""" + error2 + """<br>
                    <label>Verify Password:</label><input type='password' name='verify'/><br>
                    <label>E-mail(optional)</label> <input type='text' name='email' value='""" + email + """'/>""" + error3 + """<br>
                    <input type='submit'/>
                    <style ='text/ccs'>
                    .error { color:red; }
                    label { display:inline-block; float:left; clear:left; width:125px; text-align:left; }
                    </style>
                </form>
                """
        return self.response.out.write(form % {"error1": error1,
                                               "error2": error2,
                                               "error3": error3,
                                               "username": username,
                                               "password": password,
                                               "verify": verify,
                                               "email": email})

    def get(self):
        error_escaped1 = ''
        error_escaped2 = ''
        error_escaped3 = ''
        username = ''
        password = ''
        verify = ''
        email = ''
        self.write_form(error_escaped1, error_escaped2, error_escaped3, username, password, verify, email)

    def post(self):

        username = cgi.escape(self.request.get("username"))
        password = cgi.escape(self.request.get("password"))
        verify = cgi.escape(self.request.get("verify"))
        email = cgi.escape(self.request.get("email"))

        error_msgs = False
        error_escaped1 = ""
        error_escaped2 = ""
        error_escaped3 = ""

        if not valid_username(username):
            error1 = "Sorry, that is an invalid username."
            error_escaped1 = "<span class='error'>" + cgi.escape(error1) + "</span>"
            error_msgs = True

        if password == "":
            error2 = "You must enter a password and verify it"   # dont think i need this.
            error_escaped2 = "<span class='error'>" + cgi.escape(error2) + "</span>"
            error_msgs = True
        elif not valid_password(password):
            error2 = "Sorry, that is not a valid password."
            error_escaped2 = "<span class='error'>" + cgi.escape(error2) + "</span>"
            error_msgs = True
        elif not (password == verify):
            error2 = "Sorry, Passwords do not match!"
            error_escaped2 = "<span class='error'>" + cgi.escape(error2) + "</span>"
            error_msgs = True

        if email == "":
            pass
        elif not valid_email(email):
            error4 = "Sorry, that is not a valid email."
            error_escaped3 = "<span class='error'>" + cgi.escape(error4) + "</span>"
            error_msgs = True

        if error_msgs:
            self.write_form(error_escaped1, error_escaped2, error_escaped3, username, password, verify, email)
        else:
            self.redirect('/welcome?username=' + username)

            # TODO I want to redirect here

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup', SignupPage),
    ('/welcome', WelcomePage)
], debug=True)

#TODO Look into use of *args and **kwargs or w/e it is -- should
# for k,v in **kwargs items()
#   error{k,v}