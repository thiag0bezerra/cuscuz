from typing import Union, Optional
from contextvars import ContextVar



# Context variable para rastrear o elemento pai atual
_current_parent: ContextVar[Optional["Element"]] = ContextVar(
    "_current_parent", default=None
)


class Element:

    def __init__(
        self,
        tag: str,
        attributes: dict[str, str] | None = None,
        children: list[Union["Element", str]] | None = None,
        self_closing: bool = False,
    ):
        self.tag = tag
        self.attributes = attributes or {}
        self.children = children or []
        self.self_closing = self_closing

        # Automaticamente adiciona ao pai se houver um contexto ativo
        parent = _current_parent.get()
        if parent is not None:
            parent.add_child(self)

    def add_child(self, child: Union["Element", str]) -> None:
        self.children.append(child)

    def __enter__(self):
        self._token = _current_parent.set(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        _current_parent.reset(self._token)
        return False

    def _render_attributes(self) -> str:
        if not self.attributes:
            return ""
        return " ".join(f'{key}="{value}"' for key, value in self.attributes.items())

    def render(self) -> str:
        attr_string = self._render_attributes()
        inner = "".join(
            child.render() if isinstance(child, Element) else str(child)
            for child in self.children
        )

        if self.tag and self.self_closing and not inner:
            if attr_string:
                return f"<{self.tag} {attr_string} />"
            return f"<{self.tag} />"

        if attr_string:
            return f"<{self.tag} {attr_string}>{inner}</{self.tag}>"
        return f"<{self.tag}>{inner}</{self.tag}>"

    def __str__(self) -> str:
        return self.render()
