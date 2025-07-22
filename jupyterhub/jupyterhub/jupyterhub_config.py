c = get_config()

c.JupyterHub.bind_url = 'http://:8000'

# DummyAuthenticator for local dev (insecure — do NOT use in production)
c.JupyterHub.authenticator_class = 'dummy'
c.DummyAuthenticator.password = 'password'

# Make jovyan the admin (matches the system user you spawn as)
c.Authenticator.admin_users = {'jovyan'}

# Always spawn under the existing jovyan user
c.Spawner.default_username = 'jovyan'
c.Spawner.default_url = '/lab'

