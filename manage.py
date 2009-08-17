#!/usr/bin/python
from django.core.management import execute_manager
try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    # This is a hack to avoid the ambiguity of checkout dirs being named
    # amancay and the settings file trying to -hence- be imported as
    # 'amancay.settings', but that clashes with the amancay app dir.
    # In other words: git clone; cd amancay/; ./manage.py; fails without this.
    # You would have to rename the checkout dir to something different from
    # amancay.
    import sys
    if len(sys.argv) > 1:
        sys.argv.append('--settings=settings')
    execute_manager(settings)
