from typing import Callable, Tuple, Dict


class Local: ...

BeansDbCmd = Tuple[str, Tuple, Dict]

class DbLocal:
    def start_beansdb_transaction(self) -> None: ...

    def pop_beansdb_transaction(self) -> None: ...

    def shift_beansdb_transaction(self) -> None: ...

    def append_beansdb_commands(self, *cmds: BeansDbCmd) -> None: ...

    def insert_beansdb_commands(self, *cmds: BeansDbCmd) -> None: ...

    def add_lazy_func(self, func: Callable) -> None: ...

    def clear_lazy_funcs(self) -> None: ...

    def add_commit_handler(self, handler: Callable) -> None: ...

    def clear_commit_handlers(self) -> None: ...

    def add_rollback_handler(self, handler: Callable) -> None: ...

    def clear_rollback_handlers(self) -> None: ...
