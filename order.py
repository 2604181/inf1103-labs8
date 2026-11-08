"""
INF1103 Week 10 - Order class
"""
from order_line import OrderLine
from product import Product


class Order:
    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def add_order_line(self, product: Product, quantity: int) -> None:
        # The Order creates the OrderLine itself (this is what makes it composition)
        order_line: OrderLine = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, index: int) -> None:
        if index < 0 or index >= len(self.__order_lines):
            raise IndexError("No order line at that position.")
        del self.__order_lines[index]

    def get_order_lines(self) -> tuple[tuple[Product, int, float], ...]:
        # Plain values only: the OrderLine objects themselves never leave the Order
        lines: list[tuple[Product, int, float]] = []
        for order_line in self.__order_lines:
            lines.append((
                order_line.get_product(),
                order_line.get_quantity(),
                order_line.calculate_subtotal()
            ))
        return tuple(lines)

    def calculate_total(self) -> float:
        total: float = 0.0
        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()
        return total
