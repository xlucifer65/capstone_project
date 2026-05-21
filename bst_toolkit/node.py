from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class TrialNode:
    score: float
    params: Dict[str, Any]
    left: Optional["TrialNode"] = field(default=None, repr=False)
    right: Optional["TrialNode"] = field(default=None, repr=False)

    def __lt__(self, other: "TrialNode") -> bool:
        return self.score < other.score

    def __repr__(self) -> str:
        return f"TrialNode(score={self.score:.4f}, params={self.params})"
