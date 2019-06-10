#!/usr/bin/env python
import os
import sys
import gears_manager

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gears_django.settings")

    from django.core.management import execute_from_command_line

    args = gears_manager.parse_args()
    gears_manager.startup(args)

    try:
        execute_from_command_line([sys.executable, "runserver", "0.0.0.0:80", "--noreload"])
    finally:
        gears_manager.glo_stepper.enable(False)
