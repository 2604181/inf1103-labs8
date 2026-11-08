"""
INF1103 Week 9 - CanBeShipped interface
Interface-style abstract base class: a CONTRACT for anything that can be shipped.
"""
from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Calculate a non-negative shipping charge."""
