from config import OWNER_ID



def owner_only(user_id):

    return user_id == OWNER_ID



def has_admin_role(member):

    if member.guild_permissions.administrator:

        return True


    return False



def has_staff_role(member):

    staff_roles = [
        "Staff",
        "Moderator",
        "Admin"
    ]


    for role in member.roles:

        if role.name in staff_roles:

            return True


    return False



def can_manage(member):

    return (
        has_admin_role(member)
        or
        has_staff_role(member)
    )
