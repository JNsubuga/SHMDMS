from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as authlogin, logout as authlogout
from api.core.users.Users import Users
from api.core.modules.Modules import SystemModules
from api.core.locale.Locale import Locale
from api.core.helper.helper import Helper

from api.core.receivedDocuments.ReceivedDocuments import ReceivedDocuments
from api.core.gender.Genders import Genders
from api.core.security.Security import Security

# Create your views here.
DEFAULT_LANG = "en"

_users = Users()
_modules = SystemModules()
_locale = Locale()
_helper = Helper()

_receivedDocuments = ReceivedDocuments()
_gender = Genders()
_security = Security()

def getIcon(module):
    
    if module["code_name"] == "dashboard":
        icon = "nav-icon fas fa-tachometer-alt"
    elif module["code_name"] == "add_user":
        icon = "nav-icon fas fa-user-plus"
    elif module["code_name"] == "users":
        icon = "nav-icon fas fa-user-shield"
    elif module["code_name"] == "roles":
        icon = "nav-icon fas fa-lock"
    else:
        icon = "far fa-circle nav-icon"
    return icon

def getFullUrlPath(request, route):
    return(
        str(request.build_absolute_uri()).replace(request.get_full_path(), "") + "/" + route
    )


def getSideMenuSubmenu(request, submodules, module):
    micon = getIcon(module)
    murl = getFullUrlPath(request, module["route_name"])
    item = """<ul class="nav nav-treeview">"""
    item += f"""<li class="nav-item">
                <a href="{ murl }" class="nav-link">
                <i class="{ micon }"></i>
                <p>{module['module_name']}</p>
                </a>
            </li>"""
    for submodule in submodules:
        icon = getIcon(submodule)
        url = getFullUrlPath(request, submodule["route_name"])
        if submodule["has_children"] and len(submodule["sub_module"]) > 0:
            items = getSideMenuSubmenu(request, submodule["sub_module"], submodule)
            item += f"""
              <li class="nav-item">
                <a href="{ url }" class="nav-link">
                <i class="{ icon }"></i>
                <p>
                   {submodule['module_name']}
                    <i class="right fas fa-angle-left"></i>
                </p>
                </a>
                {items}
            </li>
            """
        else:
            item += f"""<li class="nav-item">
                        <a href="{ url }" class="nav-link">
                        <i class="{ icon }"></i>
                        <p>{submodule['module_name']}</p>
                        </a>
                    </li>
                    """
    item += """</ul>"""
    return item


def generatedSideMenu(modules, request):
    item = ""
    for module in modules:
        url = getFullUrlPath(request, module["route_name"])
        micon = getIcon(module)
        if module["has_children"] and len(module["sub_module"]) > 0:
            items = getSideMenuSubmenu(request, module["sub_module"], module)
            item += f"""
              <li class="nav-item">
                <a href="{ url }" class="nav-link">
                    <i class="{ micon }"></i>
                    <p>
                    {module['module_name']}
                        <i class="right fas fa-angle-left"></i>
                    </p>
                </a>
                {items}
            </li>
            """
        else:
            item += f"""<li class="nav-item">
                    <a href="{ url }" class="nav-link">
                    <i class="{ micon }"></i>
                    <p>
                        {module['module_name']}
                    </p>
                    </a>
                </li>"""
    return item


#############
def index(request):
    lang = DEFAULT_LANG
    if request.method == "GET":
        if request.user.is_authenticated:
            userid = request.user.pk
            modules = _modules.getSideBarModules(request, lang, userid)
            if len(modules) > 0:
                module = modules[0]
                return redirect(module["code_name"])
            else:
                return redirect("access_denied")
        else:
            return render(
                request,
                "index.html",
                {
                    "errorResponse": {"succsess": ""},
                }
            )
    else:
        inputUsername = request.POST["shmdms-input-email"]
        inputPassword = request.POST["shmdms-input-password"]
        # remember_me = request.POST["remeberme"]
        #####################################################
        if not inputUsername:
            errorResponse = {"success": False, "message": "Username are required"}
        elif not inputPassword:
            errorResponse = {"success": False, "message": "Password are required"}
        else:
            unilogin = _users.EmailOrUsernameLogin(request, lang, inputUsername)
            if not unilogin["success"]:
                errorResponse = {
                    "success": False,
                    "message": "Username or email doesen't exist!!!"
                }
            else:
                username = unilogin["username"]
                user = authenticate(username=username, password=inputPassword)
                if user:
                    errorResponse ={
                        "user_id": user.pk,
                        "user": unilogin,
                        "message": "",
                        "success": True
                    }
                    authlogin(request, user)
                    ########################
                    request.session["auth_token"] = unilogin["token"]
                    modules = _modules.getSideBarModules(request, lang, user.pk)
                    if len(modules) > 0:
                        module = modules[0]
                        redirect_url =(
                            module["code_name"]
                            if "next" not in request.GET or not request.GET["next"] else request.GET["next"]
                        )
                        return redirect(redirect_url)
                    else:
                        authlogout(request)
                        return redirect("access_denied")
                else:
                    errorResponse = {
                        "success": False,
                        "message": "Invali login details",
                    }
        return render(
            request,
            "index.html",
            {
                "errorResponse": {"success": ""}
            }
        )

def logout(request):
    authlogout(request)
    redirect_url = (
        "home"
        if "next" not in request.GET or not request.GET["next"]
        else request.GET["next"]
    )
    return redirect(redirect_url)

def dashboard(request):
    lang = DEFAULT_LANG
    if request.user.is_authenticated:
        userid = request.user.pk
        modules = _modules.getSideBarModules(request, lang, userid)
        sidemenu = generatedSideMenu(modules, request)
        auth_user = _users.getAuthUserById(request, lang, userid)
        return render(
            request,
            "dashboard.html",
            {
                "modules": modules,
                "auth_user": auth_user,
                "sidemenu": sidemenu,
            },
        )

    else:
        return redirect("home")

def users(request):
    lang = DEFAULT_LANG
    if request.user.is_authenticated:
        userid = request.user.pk
        modules = _modules.getSideBarModules(request, lang, userid)
        auth_user = _users.getAuthUserById(request, lang, userid)
        sidemenu = generatedSideMenu(modules, request)
        return render(
            request,
            "users/users.html",
            {
                "modules": modules,
                "auth_user": auth_user,
                "sidemenu": sidemenu,
            },
        )
    else:
        return redirect("home")

def Adduser(request):
    lang = DEFAULT_LANG
    if request.user.is_authenticated:
        userid = request.user.pk
        modules = _modules.getSideBarModules(request, lang, userid)
        auth_user = _users.getAuthUserById(request, lang, userid)
        sidemenu = generatedSideMenu(modules, request)
        #################
        genders = _gender.getAllGenders(request, lang)
        roles = _security.getAllSecurityGroups(request, lang)
        permissions = _security.getAllPermissions(request, lang)
        ################
        return render(
            request,
            "users/add-user.html",
            {
                "modules": modules,
                "genders": genders,
                "roles": roles,
                "permissions": permissions,
                "auth_user": auth_user,
                "sidemenu": sidemenu,
            },
        )
    else:
        return redirect("home")
    
def updateuser(request, userid):
    lang = DEFAULT_LANG
    if request.user.is_authenticated:
        authuserid = request.user.pk
        modules = _modules.getSideBarModules(request, lang, authuserid)
        auth_user = _users.getAuthUserById(request, lang, authuserid)
        #################
        genders = _gender.getAllGenders(request, lang)
        roles = _security.getAllSecurityGroups(request, lang)
        permissions = _security.getAllPermissions(request, lang)
        sidemenu = generatedSideMenu(modules, request)
        selected_user = _users.getAuthUserById(request, lang, userid)
        return render(
            request,
            "users/update-user.html",
            {
                "modules": modules,
                "genders": genders,
                "selected_user": selected_user,
                "roles": roles,
                "permissions": permissions,
                "auth_user": auth_user,
                "sidemenu": sidemenu,
            },
        )
    else:
        return redirect("home")

def Roles(request):
    lang = DEFAULT_LANG
    if request.user.is_authenticated:
        userid = request.user.pk
        modules = _modules.getSideBarModules(request, lang, userid)
        auth_user = _users.getAuthUserById(request, lang, userid)
        sidemenu = generatedSideMenu(modules, request)
        permissions = _security.getAllPermissions(request, lang)
        return render(
            request,
            "roles.html",
            {
                "modules": modules,
                "auth_user": auth_user,
                "permissions": permissions,
                "sidemenu": sidemenu,
            },
        )
    else:
        return redirect("home")

def AccessDenied(request):
    lang = DEFAULT_LANG
    return render(
        request,
        "access-denied.html",
        {},
    )

def receivedDocuments(request):
    lang = DEFAULT_LANG
    if request.user.is_authenticated:
        userid = request.user.pk 
        modules = _modules.getSideBarModules(request, lang, userid)
        auth_user = _users.getAuthUserById(request, lang, userid)
        sidemenu = generatedSideMenu(modules, request)

        receivedDocuments = _receivedDocuments.getAllReceivedDocuments(request, lang)

        return render (
            request,
            "receivedDocuments/receivedDocuments.html",
            {
                "modules": modules,
                "auth_user": auth_user,
                "sidemenu": sidemenu,
                "receivedDocuments": receivedDocuments
            }
        )
    else:
        return redirect("home")

def registerReceivedDocument(request):
    lang = DEFAULT_LANG
    if request.user.is_authenticated:
        userid = request.user.pk
        modules = _modules.getSideBarModules(request, lang, userid)
        auth_user = _users.getAuthUserById(request, lang, userid)
        sidemenu = generatedSideMenu(modules, request)

        return render(
            request,
            "receivedDocuments/registerReceivedDocument.html",
            {
                "modules": modules,
                "auth_user": auth_user,
                "sidemenu": sidemenu
            }
        )
    else:
        return redirect("home")