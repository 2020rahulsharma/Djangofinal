from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from service.utility.DataValidator import DataValidator
from service.service.UserService import UserService


class LoginCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form["login_id"] = requestForm["login_id"]
        self.form["password"] = requestForm["password"]

    def input_validation(self):
         
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["login_id"])):
            inputError["login_id"] = "Login can not be null"
            self.form["error"] = True
        if (DataValidator.isNull(self.form["password"])):
            inputError["password"] = "Password can not be null"
            self.form["error"] = True

        return self.form["error"]

    def display(self, request, params={}):
        res = render(request, self.get_template())
        return res

    def submit(self, request, params={}):
        if (self.input_validation()):
            return render(request, self.get_template(), {"form": self.form})
        else:
            user = self.get_service().authenticate(self.form)
            if (user is None):
                self.form["message"] = "Invalid ID or Password"
                res = render(request, self.get_template(), {"form": self.form})
            else:
                request.session["user"] = user
                self.form["message"] = "LOGIN SUCCESSFULLY"
                res = redirect('/ORS/Welcome')
        return res

    # Template html of Role page    
    def get_template(self):
        return "ors/Login.html"

        # Service of Role

    def get_service(self):
        return UserService()
