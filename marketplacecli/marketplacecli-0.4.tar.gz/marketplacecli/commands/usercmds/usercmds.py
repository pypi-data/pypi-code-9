__author__ = "UShareSoft"

from texttable import Texttable
from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from marketplacecli.utils import org_utils
from ussclicore.utils import printer
from ussclicore.utils import generics_utils
from marketplacecli.utils import marketplace_utils
from marketplace.objects.marketplace import *


class UserCmds(Cmd, CoreGlobal):
    """Manage users : list users, update users, update roles"""

    cmd_name = "user"

    def __init__(self):
        super(UserCmds, self).__init__()

    def arg_info(self):
        do_parser = ArgumentParser(prog=self.cmd_name + " info", add_help=True,
                                   description="Displays informations of provided user")
        return do_parser

    def do_info(self, args):
        try:
            # call UForge API
            printer.out("Getting user [" + self.login + "] ...")
            user = self.api.Users(self.login).Get()

            if user is None:
                printer.out("user " + self.login + "does not exist", printer.ERROR)
            else:
                table = Texttable(200)
                table.set_cols_align(["c", "l", "c", "c", "c", "c", "c", "c"])
                table.header(
                    ["Login", "Email", "Lastname", "Firstname", "Created", "Active", "Promo Code", "Creation Code"])
                table.add_row([user.loginName, user.email, user.surname, user.firstName,
                               user.created.strftime("%Y-%m-%d %H:%M:%S"), "X", user.promoCode, user.creationCode])
                print table.draw() + "\n"
            return 0
        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_info()
        except Exception as e:
            return marketplace_utils.handle_uforge_exception(e)

    def help_info(self):
        do_parser = self.arg_info()
        do_parser.print_help()

    def arg_create(self):
        do_parser = ArgumentParser(prog=self.cmd_name + " create", add_help=True, description="Creates a new user")
        mandatory = do_parser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--account', dest='account', required=True, help="the login name of the user to create")
        mandatory.add_argument('--email', dest='email', required=True, help="the email of the user to create")
        mandatory.add_argument('--code', dest='code', required=True,
                               help="the creation code (subscription profile) to be used to create the user account")
        optional = do_parser.add_argument_group("optional arguments")
        optional.add_argument('--accountPassword', dest='accountPassword', required=False,
                              help="the new user account password")
        optional.add_argument('--org', dest='org', required=False,
                              help="the organization in which the user should be created")
        optional.add_argument('--disable', dest='disable', required=False,
                              help="flag to de-activate the account during the creation")
        return do_parser

    def do_create(self, args):
        try:
            # add arguments
            do_parser = self.arg_create()
            try:
                do_args = do_parser.parse_args(args.split())
            except SystemExit as e:
                return

            # call UForge API
            printer.out("Creating user account [" + do_args.account + "] ...")

            # create a user manually
            new_user = user()
            new_user.loginName = do_args.account
            new_user.password = do_args.accountPassword
            new_user.creationCode = do_args.code
            new_user.email = do_args.email
            new_user.password = do_args.accountPassword

            if do_args.org:
                org = do_args.org
            else:
                org = None
            if do_args.disable:
                new_user.active = False
            else:
                new_user.active = True

            # Send the create user request to the server
            new_user = self.api.Users(self.login).Create("true", "true", org, "false", "false", "false", new_user)

            if new_user is None:
                printer.out("No information about new user available", printer.ERROR)
            else:
                table = Texttable(200)
                table.set_cols_align(["c", "l", "c", "c", "c", "c", "c", "c"])
                table.header(
                    ["Login", "Email", "Lastname", "Firstname", "Created", "Active", "Promo Code", "Creation Code"])
                table.add_row([new_user.loginName, new_user.email, new_user.surname, new_user.firstName,
                               new_user.created.strftime("%Y-%m-%d %H:%M:%S"), "X", new_user.promoCode,
                               new_user.creationCode])
                print table.draw() + "\n"
            return 0
        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_create()
        except Exception as e:
            return marketplace_utils.handle_uforge_exception(e)

    def help_create(self):
        do_parser = self.arg_create()
        do_parser.print_help()

    def arg_list(self):
        do_parser = ArgumentParser(prog=self.cmd_name + " list", add_help=True,
                                   description="List the users registered to the platform")
        return do_parser

    def do_list(self, args):
        try:

            # call UForge API
            printer.out("Getting users...")
            users = self.api.Users(self.login).Getall(None, None, None)

            if users is None:
                printer.out("No user")
            else:
                table = Texttable(200)
                table.set_cols_align(["c", "l", "c", "c", "c", "c", "c", "c"])
                table.header(
                    ["Login", "Email", "Lastname", "Firstname", "Created", "Active", "Promo Code", "Creation Code"])
                for u in users.users.user:
                    table.add_row([u.loginName, u.email, u.surname, u.firstName,
                                   u.created.strftime("%Y-%m-%d %H:%M:%S"), "X", u.promoCode, u.creationCode])
                print table.draw() + "\n"
            return 0
        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_info()
        except Exception as e:
            return marketplace_utils.handle_uforge_exception(e)

    def help_list(self):
        do_parser = self.arg_list()
        do_parser.print_help()
