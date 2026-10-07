"""In-memory browser frame adapter. No camera recording or disk capture."""
def service(app):
    return app.frames
