"""Parser/serializador do formato .msg do AtlusScript (messagescript do P5R).

Objetivos:
- Round-trip exato: ``serialize_msg(parse_msg(t)) == t``.
- Separar o texto visivel das tags de controle (ex.: ``[f 2 1]``, ``[e]``, ``[n]``),
  para que a traducao altere so o texto e preserve todas as tags.

O formato e uma sequencia de blocos com cabecalho ``[msg NOME [FALANTE]]`` ou
``[sel NOME]`` seguidos do corpo (texto + tags + quebras de linha) ate o proximo
cabecalho. Qualquer conteudo antes do primeiro cabecalho e guardado como preambulo.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# Cabecalho: [msg nome [falante]]  /  [sel nome]
HEADER_RE = re.compile(r"^\[(msg|sel)\s+([^\s\]]+)(?:\s+\[([^\]]*)\])?\]\s*$")
# Qualquer tag de controle entre colchetes.
TAG_RE = re.compile(r"\[[^\]]*\]")


@dataclass
class Message:
    """Um bloco de mensagem (dialogo ``msg`` ou selecao ``sel``)."""

    kind: str  # "msg" ou "sel"
    name: str
    speaker: str | None
    header_line: str  # cabecalho verbatim (preserva o round-trip exato)
    body_lines: list[str] = field(default_factory=list)

    @property
    def body(self) -> str:
        return "\n".join(self.body_lines)

    def set_body(self, text: str) -> None:
        self.body_lines = text.split("\n")


@dataclass
class MessageFile:
    preamble: list[str] = field(default_factory=list)
    messages: list[Message] = field(default_factory=list)


def parse_msg(text: str) -> MessageFile:
    """Converte o conteudo de um .msg em ``MessageFile``."""
    lines = text.split("\n")
    mf = MessageFile()
    current: Message | None = None

    for line in lines:
        header = HEADER_RE.match(line)
        if header:
            current = Message(
                kind=header.group(1),
                name=header.group(2),
                speaker=header.group(3),
                header_line=line,
            )
            mf.messages.append(current)
        elif current is None:
            mf.preamble.append(line)
        else:
            current.body_lines.append(line)

    return mf


def serialize_msg(mf: MessageFile) -> str:
    """Reconstroi o texto .msg a partir de um ``MessageFile`` (round-trip exato)."""
    out: list[str] = list(mf.preamble)
    for msg in mf.messages:
        out.append(msg.header_line)
        out.extend(msg.body_lines)
    return "\n".join(out)


def extract_tags(body: str) -> list[str]:
    """Lista todas as tags de controle (ex.: ``['[f 2 1]', '[e]']``)."""
    return TAG_RE.findall(body)


def visible_text(body: str) -> str:
    """Retorna so o texto visivel (sem tags), util para QA de tamanho."""
    return TAG_RE.sub("", body)
