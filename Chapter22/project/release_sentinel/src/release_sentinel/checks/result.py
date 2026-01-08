from dataclasses import dataclass

OK = "OK"
WARN = "WARN"
CRIT = "CRIT"

@dataclass
class CheckResult:
    status: str
    message: str
