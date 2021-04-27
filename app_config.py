import os

CLIENT_ID = "e46e77ca-183c-4aaa-ae3c-4ae02ac2a94e" # Application (client) ID of app registration

CLIENT_SECRET = "_-PRR3Q.3A~nY5CnX8C0iL9~e3Q~0E~e0l" # Placeholder - for use ONLY during testing.
# In a production app, we recommend you use a more secure method of storing your secret,
# like Azure Key Vault. Or, use an environment variable as described in Flask's documentation:
# https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# if not CLIENT_SECRET:
#     raise ValueError("Need to define CLIENT_SECRET environment variable")

AUTHORITY = "https://login.microsoftonline.com/c1eefed8-1881-49e4-b13b-851bca2ca106"  # For multi-tenant app
# AUTHORITY = "https://login.microsoftonline.com/Enter_the_Tenant_Name_Here"

REDIRECT_PATH = "/getAToken"  # Used for forming an absolute URL to your redirect URI.
                              # The absolute URL must match the redirect URI you set
                              # in the app's registration in the Azure portal.

# You can find more Microsoft Graph API endpoints from Graph Explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer
#ENDPOINT = 'https://graph.microsoft.com/v1.0/users'  # This resource requires no admin consent
ENDPOINT = 'https://graph.microsoft.com/beta/me/appRoleAssignments'  # role assignments.


# You can find the proper permission names from this document
# https://docs.microsoft.com/en-us/graph/permissions-reference
SCOPE = ["User.ReadBasic.All"]

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session

USERNAME = "su123mf123@outlook.com"
