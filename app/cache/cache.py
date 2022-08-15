import streamlit as st
from streamlit import session_state as _state

_PERSIST_STATE_KEY = f"{__name__}_PERSIST"


def persist(key: str) -> str:
    if _PERSIST_STATE_KEY not in _state:
        _state[_PERSIST_STATE_KEY] = set()

    _state[_PERSIST_STATE_KEY].add(key)

    return key


def load_widget_state():
    if _PERSIST_STATE_KEY in _state:
        _state.update(
            {
                key: value
                for key, value in _state.items()
                if key in _state[_PERSIST_STATE_KEY]
            }
        )

    init_cache()


def init_cache():
    if "page" not in st.session_state:
        st.session_state.update(
            {
                "page": "dashboard",
            }
        )
