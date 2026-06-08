"""autoresearch.config — customer-config skill (CFG-INIT/VAL/SHOW-*)."""
from .init import run_init
from .validate import run_validate
from .show import run_show
from .keyring_cli import run_keyring

__all__ = ["run_init", "run_validate", "run_show", "run_keyring"]
