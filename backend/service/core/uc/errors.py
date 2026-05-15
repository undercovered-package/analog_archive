class MemberNotFoundError(Exception):
    pass


# Backward compatibility alias
UserNotFoundError = MemberNotFoundError


class TeamNotFoundError(Exception):
    pass
