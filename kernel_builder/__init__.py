import sh
import logging
from kernel_builder.utils.env import verbose_enabled
from kernel_builder.config.config import LOGFILE
from kernel_builder.utils.log import configure_log

configure_log(
    logfile=LOGFILE,
    level=logging.DEBUG if verbose_enabled() else logging.INFO,
)

if verbose_enabled():
    sh.Command._call_args.update({"tee": True})
