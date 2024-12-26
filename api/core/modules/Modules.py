# All Things related to modules
from datetime import datetime
from django.core.validators import validate_email
from django.core.paginator import Paginator
from django.utils import timezone
from api.core.helper import helper, webconfig
from api.models import *
from django.db.models import Count
from django.db.models import Q
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


# helper class
# master module class
class SystemModules:
    def __init__(self):
        self.help = helper.Helper()

    # Get All Modules
    def getMainModules(self, request, lang):
        results = []
        main_modules = Module.objects.filter(
            Q(is_disabled=False) and Q(is_a_sub_module=False)
        ).order_by("sort_value")
        # main module is compulsory
        for main_module in main_modules:
            module_name = getattr(main_module, f"{lang}_module_name")
            # print(module_name)
            submodules = None
            results.append(
                {
                    "module_id": main_module.pk,
                    "module_name": module_name,
                    "sub_module": (
                        self.getSubModules(request, lang, main_module.pk)
                        if main_module.has_children
                        and len(self.getSubModules(request, lang, main_module.pk))
                        else None
                    ),
                    "code_name": main_module.code_name,
                    "route_name": main_module.route_name,
                    "main_module_id": main_module.main_module_id,
                    "depth": main_module.depth,
                    "is_a_sub_module": main_module.is_a_sub_module,
                    "sort_value": main_module.sort_value,
                    "has_children": main_module.has_children,
                    "created": main_module.created,
                    "is_disabled": main_module.is_disabled,
                    "message": "",
                    "success": True,
                }
            )
        return results

    def has_module_permission(self, request, lang, user_id, moduleid):
        has_permission = False
        # check if module has permission
        if Permission.objects.filter(
            module=Module(pk=moduleid)
        ).exists():  # TO DO: i ommited is_module_permission filter
            # Module has permission .. lets proceed
            # get module permission
            module_permissions = Permission.objects.filter(module=Module(pk=moduleid))
            # check if the user had that module permission in user permission table
            for module_permission in module_permissions:
                if (
                    UserPermission.objects.filter(
                        permission=Permission(pk=module_permission.pk)
                    )
                    .filter(has_permission=True)
                    .filter(user=User(pk=user_id))
                    .exists()
                ):
                    has_permission = True
            return has_permission
        else:
            # module has no permission so it must not appear in the module list
            return has_permission

    # Get All Modules
    def getSideBarModules(self, request, lang, user_id):
        results = []
        smodules = SideMenu.objects.filter(is_disabled=False).order_by("sort_value")
        # main module is compulsory
        for smodule in smodules:
            module_id = smodule.module.pk
            # if user has permission on module
            if self.has_module_permission(request, lang, user_id, module_id):
                module = self.getModuleById(request, lang, module_id, user_id)
                results.append(module)
        # Get sub modules as main modules in which the user has permission but don't have a main module in the menu
        merge_modules = self.mergeSubModulesFromUserPermissions(
            request,
            lang,
            user_id,
            results,
        )
        return merge_modules

    def mergeSubModulesFromUserPermissions(self, request, lang, user_id, allmodules):
        userpermissions = UserPermission.objects.filter(user=User(pk=user_id)).filter(
            has_permission=True
        )
        for userpermission in userpermissions:
            if not (userpermission.permission.module == None) and (
                userpermission.permission.module.is_a_sub_module
            ):
                moduleid = userpermission.permission.module.pk
                module = self.getModuleById(request, lang, moduleid, user_id)
                if not self.doesModuleAlreadyExistInMenu(
                    request, lang, allmodules, moduleid, user_id
                ):
                    allmodules.append(module)
        return allmodules

    #######
    #######
    # Get All Modules
    def getAllModules(self, request, lang):
        results = []
        modules = Module.objects.filter(is_disabled=False).order_by("sort_value")
        # main module is compulsory
        for module in modules:
            module_name = getattr(module, f"{lang}_module_name")
            # print(module_name)
            results.append(
                {
                    "module_id": module.pk,
                    "module_name": module_name,
                    "route_name": module.route_name,
                    "code_name": module.code_name,
                    "depth": module.depth,
                    "sort_value": module.sort_value,
                    "has_children": module.has_children,
                    "main_module_id": module.main_module_id,
                    "is_a_sub_module": module.is_a_sub_module,
                    "created": module.created,
                    "is_disabled": module.is_disabled,
                    "message": "",
                    "success": True,
                }
            )
        return results

    #######
    # Get modules by id
    def getModuleById(self, request, lang, module_id, userid=None):
        # First check if these modules exist
        if Module.objects.filter(pk=module_id).exists():
            # filter in all of them and geta single record that matches
            module = Module.objects.filter(pk=module_id).get()
            # print(module.pk)
            # return a map of found module if it exists or other wise return None
            module_name = getattr(module, f"{lang}_module_name")
            return {
                "module_id": module.pk,
                "module_name": module_name,
                "route_name": module.route_name,
                "code_name": module.code_name,
                "depth": module.depth,
                "sort_value": module.sort_value,
                "has_children": module.has_children,
                "main_module_id": module.main_module_id,
                "sub_module": (
                    self.getSubModules(request, lang, module.pk, userid)
                    if module.has_children
                    else None
                ),
                "is_a_sub_module": module.is_a_sub_module,
                "created": module.created,
                "is_disabled": module.is_disabled,
            }
        else:
            return None

    def doesModuleAlreadyExistInMenu(
        self, request, lang, allmodules, moduleid, userid=None
    ):
        results = []
        for module in allmodules:
            # return a map of found module if it exists or other wise return None
            if not module["has_children"]:
                if module["module_id"] == moduleid:
                    results.append(module)
            else:
                submodules = module["sub_module"]
                result = self.doesSubModuleAlreadyExistInMenu(
                    request,
                    lang,
                    submodules,
                    moduleid,
                    userid,
                )
                results.extend(result)
        return True if (len(results)) > 0 else False

    def doesSubModuleAlreadyExistInMenu(
        self, request, lang, allsubmodules, moduleid, userid=None
    ):
        results = []
        for module in allsubmodules:
            # return a map of found module if it exists or other wise return None
            if not module["has_children"]:
                if module["module_id"] == moduleid:
                    results.append(module)
            else:
                submodules = module["sub_module"]
                results = self.doesSubModuleAlreadyExistInMenu(
                    request, lang, submodules, moduleid, userid=None
                )
                results.extend(results)
        return results

    # update module name
    # Get modules by id
    def updateModuleName(self, request, lang, module_id, module_name):
        # First check if these modules exist
        # print(field_name)
        if Module.objects.filter(pk=module_id).exists():
            # filter in all of them and geta single record that matches
            module = Module.objects.filter(pk=module_id)
            update_dict = {f"{lang}_module_name": module_name}
            module.update(**update_dict)
            # print(module.pk)
            # # return a map of found module if it exists or other wise return None
            return {"message": "Module updated succesfully", "status": "success"}
        else:
            return None

    ##########
    # Get sub modules
    def getSubModules(self, request, lang, moduleid, userid=None):
        results = []
        # print(moduleid)
        # First check if these modules exist
        if Module.objects.filter(pk=moduleid).exists():
            # filter in all of them and geta single record that matches
            submodules = Module.objects.filter(
                Q(is_disabled=False) and Q(main_module_id=moduleid)
            ).order_by("sort_value")
            # print(module.pk)
            # return a map of found module if it exists or other wise return None
            for submodule in submodules:
                module_name = getattr(submodule, f"{lang}_module_name")
                if not userid == None:
                    if self.has_module_permission(request, lang, userid, submodule.pk):
                        results.append(
                            {
                                "module_id": submodule.pk,
                                "module_name": module_name,
                                "route_name": submodule.route_name,
                                "code_name": submodule.code_name,
                                "depth": submodule.depth,
                                "sort_value": submodule.sort_value,
                                "has_children": submodule.has_children,
                                "main_module_id": submodule.main_module_id,
                                "sub_module": (
                                    self.getSubModules(request, lang, submodule.pk)
                                    if submodule.has_children
                                    else None
                                ),
                                "is_a_sub_module": submodule.is_a_sub_module,
                                "created": submodule.created,
                                "is_disabled": submodule.is_disabled,
                            }
                        )
                else:
                    results.append(
                        {
                            "module_id": submodule.pk,
                            "module_name": module_name,
                            "route_name": submodule.route_name,
                            "code_name": submodule.code_name,
                            "depth": submodule.depth,
                            "sort_value": submodule.sort_value,
                            "has_children": submodule.has_children,
                            "main_module_id": submodule.main_module_id,
                            "sub_module": (
                                self.getSubModules(request, lang, submodule.pk)
                                if submodule.has_children
                                else None
                            ),
                            "is_a_sub_module": submodule.is_a_sub_module,
                            "created": submodule.created,
                            "is_disabled": submodule.is_disabled,
                        }
                    )
            return results
        else:
            return None

    # update module name
    # Get modules by id
    def disableModule(self, request, lang, module_id):
        # First check if these modules exist
        if Module.objects.filter(pk=module_id).exists():
            # filter in all of them and geta single record that matches
            module = Module.objects.filter(pk=module_id)
            condition = True if not module.get().is_disabled else False
            message = "enabled" if not module.get().is_disabled else "disabled"
            module.update(is_disabled=condition)
            # print(module.pk)
            # # return a map of found module if it exists or other wise return None
            return {"message": f"Module {message} succesfully", "status": "success"}
        else:
            return None

    ##########
    # Get sub modules
    def getDashboardMenu(self, request, lang):
        results = []
        # First check if these modules exist
        # filter in all of them and geta single record that matches
        dashboard_modules = DashboardMenu.objects.filter(is_disabled=False).order_by(
            "sort_value"
        )
        for dashboard_module in dashboard_modules:
            module_id = dashboard_module.module.pk
            # if user has permission on module
            if self.has_module_permission(request, lang, module_id):
                module = self.getModuleById(request, lang, module_id)
                results.append(module)
            # print(module_results)
        # objects.filter(Q(is_disabled=False) and Q(main_module_id=moduleid)).order_by('sort_value')
        # print(module.pk)
        # return a map of found module if it exists or other wise return None
        # for submodule in submodules:
        #     module_name = getattr(submodule, f"{lang}_module_name")
        #     results.append({
        #         "module_id": submodule.pk,
        #         "module_name": module_name,
        #         "route_name":  submodule.route_name,
        #         "code_name": submodule.code_name,
        #         "depth": submodule.depth,
        #         "sort_value": submodule.sort_value,
        #         "has_children": submodule.has_children,
        #         "main_module_id": submodule.main_module_id,
        #         "sub_module": self.getSubModules(request, lang, submodule.pk) if submodule.has_children else None,
        #         "is_a_sub_module": submodule.is_a_sub_module,
        #         "created": submodule.created,
        #         "is_disabled": submodule.is_disabled,
        #         "has_been_modified":submodule.has_been_modified,
        #         "last_modified": submodule.last_modified
        #     })
        return results
