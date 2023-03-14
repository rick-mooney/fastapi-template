import sys
import os
from importlib import import_module
import sentry_sdk

excluded_dirs = ['tests', '__pycache__']
working_dir = "app/scripts"

sentry_sdk.init(dsn=os.environ.get("SENTRY_URL"))

# usage: from the backend dir, run python manage.py ${file_name}
# if your script is in a subdir, reference the subdir in the file path. e.g. python manage.py migrations/example

if __name__ == "__main__":
    scripts = []
    for dirpath, dirnames, filenames in os.walk(working_dir):
        if dirpath not in excluded_dirs:
            for filename in [f for f in filenames if f.endswith(".py")]:
                scripts.append(os.path.join(dirpath, filename).replace(f"{working_dir}/", ''))
    func = f"{sys.argv[1]}"
    inputs = sys.argv[2:]
    if f"{func}.py" in scripts:
        try:
            module = import_module(f"app.scripts.{func.replace('/', '.')}")
            module.handle(inputs)
        except Exception as e:
            with sentry_sdk.push_scope() as scope:
                sentry_sdk.capture_exception(e)
            print(e)
    else:
        raise Exception(f"Script {func} not found")
