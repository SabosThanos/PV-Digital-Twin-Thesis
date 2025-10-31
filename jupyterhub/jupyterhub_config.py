c = get_config()

# Hub listening address
c.JupyterHub.bind_url = 'http://:8000'

# DummyAuthenticator for local testing (accepts any password)
c.JupyterHub.authenticator_class = 'dummy'
c.DummyAuthenticator.password = 'password'

# Make 'ubuntu' the admin
c.Authenticator.admin_users = {'ubuntu'}

# Always spawn under the existing 'ubuntu' system user
c.Spawner.default_username = 'ubuntu'
c.Spawner.default_url = '/lab'