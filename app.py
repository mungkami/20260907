from __future__ import annotations

from typing import TypedDict

import streamlit as st


class Todo(TypedDict):
    id: int
    title: str
    completed: bool


def initialize_state() -> None:
    if "todos" not in st.session_state:
        st.session_state.todos: list[Todo] = []
    if "next_todo_id" not in st.session_state:
        st.session_state.next_todo_id = 1


def add_todo(title: str) -> None:
    st.session_state.todos.append(
        {
            "id": st.session_state.next_todo_id,
            "title": title.strip(),
            "completed": False,
        }
    )
    st.session_state.next_todo_id += 1


def render_summary(todos: list[Todo]) -> None:
    completed_count = sum(todo["completed"] for todo in todos)
    pending_count = len(todos) - completed_count
    completed_column, pending_column, total_column = st.columns(3)
    completed_column.metric("완료", completed_count)
    pending_column.metric("미완료", pending_count)
    total_column.metric("전체", len(todos))


def render_todo_list() -> None:
    todos: list[Todo] = st.session_state.todos
    if not todos:
        st.info("아직 등록된 할 일이 없습니다.")
        return

    todos_to_delete: list[int] = []
    for todo in todos:
        checkbox_column, title_column, delete_column = st.columns([0.08, 0.82, 0.1])
        is_completed = checkbox_column.checkbox(
            "완료",
            value=todo["completed"],
            key=f"todo_completed_{todo['id']}",
            label_visibility="collapsed",
        )
        todo["completed"] = is_completed

        title = f"~~{todo['title']}~~" if is_completed else todo["title"]
        title_column.markdown(title)
        if delete_column.button("삭제", key=f"todo_delete_{todo['id']}"):
            todos_to_delete.append(todo["id"])

    if todos_to_delete:
        st.session_state.todos = [
            todo for todo in todos if todo["id"] not in todos_to_delete
        ]
        st.rerun()


def main() -> None:
    st.set_page_config(page_title="할 일 관리", page_icon="✅", layout="centered")
    initialize_state()

    st.title("할 일 관리")
    st.caption("오늘 해야 할 일을 한곳에서 관리하세요.")

    with st.form("add_todo_form", clear_on_submit=True):
        title = st.text_input("새 할 일", placeholder="예: 장보기 목록 정리")
        submitted = st.form_submit_button("할 일 추가", type="primary", use_container_width=True)
        if submitted:
            if title.strip():
                add_todo(title)
                st.rerun()
            st.warning("할 일 내용을 입력해 주세요.")

    st.divider()
    render_summary(st.session_state.todos)
    st.subheader("할 일 목록")
    render_todo_list()


if __name__ == "__main__":
    main()