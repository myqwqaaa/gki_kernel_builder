import sys
import sh
from kernel_builder.utils.env import verbose_enabled

if verbose_enabled():
    sh.Command._call_args.update({"out": sys.stdout, "err": sys.stderr})
