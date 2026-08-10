import app.config


def pytest_configure():

    app.config.ENABLE_PROMPT_LOG = False