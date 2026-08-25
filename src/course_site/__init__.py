"""Course site generation for *LLMs & You: Attention is All You Need*.

The site is derived, not written. ``data/*.yml`` is the single source of truth;
this package validates it (:mod:`models`), dates it (:mod:`calendar`), loads it
(:mod:`loaders`), and renders it (:mod:`macros`, :mod:`gen_sessions`).
"""

__version__ = "0.1.0"
