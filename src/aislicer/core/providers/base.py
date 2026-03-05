from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class ModelResult:
    raw_text: str
    latency_ms: int

class ModelProvider(ABC):
    @abstractmethod
    def generate(self, *, prompt: str, model: str) -> ModelResult:
        raise NotImplementedError
