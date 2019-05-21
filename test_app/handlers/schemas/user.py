import trafaret as t

from test_app.models.db import Role


USER_QUERY = t.Dict({
    t.Key('role', optional=True): t.String(),
    t.Key('first_name', optional=True): t.String(),
    t.Key('last_name', optional=True): t.String(),
    t.Key('email', optional=True): t.String(),
})


USER_ADD = t.Dict({
    t.Key('role'): t.Enum(Role.admin.name, Role.manager.name, Role.user.name),
    t.Key('first_name'): t.String(),
    t.Key('last_name'): t.String(),
    t.Key('email'): t.String(),
})
