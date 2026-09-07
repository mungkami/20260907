from __future__ import annotations

from collections import defaultdict
from datetime import date
from typing import TypedDict

import streamlit as st


PAGE_TITLE = "독서 기록"
DATE_FORMAT = "%Y-%m"


class Book(TypedDict):
    id: int
    name: str
    author: str
    added_on: date
    read: bool


def initialize_state() -> None:
    if "books" not in st.session_state:
        st.session_state.books: list[Book] = []
    if "next_book_id" not in st.session_state:
        st.session_state.next_book_id = 1


def add_book(name: str, author: str, added_on: date) -> None:
    st.session_state.books.append(
        {
            "id": st.session_state.next_book_id,
            "name": name.strip(),
            "author": author.strip(),
            "added_on": added_on,
            "read": False,
        }
    )
    st.session_state.next_book_id += 1


def render_summary(books: list[Book]) -> None:
    read_count = sum(book["read"] for book in books)
    unread_count = len(books) - read_count
    read_column, unread_column, total_column = st.columns(3)
    read_column.metric("읽은 책", read_count)
    unread_column.metric("읽을 책", unread_count)
    total_column.metric("전체 도서", len(books))


def render_book_list() -> None:
    books: list[Book] = st.session_state.books
    if not books:
        st.info("아직 등록된 책이 없습니다.")
        return

    books_to_delete: list[int] = []
    for book in books:
        read_column, book_column, delete_column = st.columns([0.08, 0.77, 0.15])
        is_read = read_column.checkbox(
            "읽음",
            value=book["read"],
            key=f"book_read_{book['id']}",
            label_visibility="collapsed",
        )
        book["read"] = is_read

        book_title = f"~~{book['name']}~~" if is_read else f"**{book['name']}**"
        book_column.markdown(f"{book_title}  \n{book['author']} · {book['added_on']:%Y년 %m월 %d일}")
        if delete_column.button("삭제", key=f"book_delete_{book['id']}"):
            books_to_delete.append(book["id"])

    if books_to_delete:
        st.session_state.books = [
            book for book in books if book["id"] not in books_to_delete
        ]
        st.rerun()


def render_monthly_statistics(books: list[Book]) -> None:
    if not books:
        st.info("도서를 등록하면 월별 통계가 표시됩니다.")
        return

    monthly_counts: dict[str, dict[str, int]] = defaultdict(
        lambda: {"등록 도서": 0, "읽은 도서": 0}
    )
    for book in books:
        month = book["added_on"].strftime(DATE_FORMAT)
        monthly_counts[month]["등록 도서"] += 1
        if book["read"]:
            monthly_counts[month]["읽은 도서"] += 1

    chart_data = {
        category: {month: counts[category] for month, counts in sorted(monthly_counts.items())}
        for category in ("등록 도서", "읽은 도서")
    }
    st.bar_chart(chart_data)


def main() -> None:
    st.set_page_config(page_title=PAGE_TITLE, page_icon="📚", layout="centered")
    initialize_state()

    st.title("독서 기록")
    st.caption("읽고 싶은 책과 독서 진행 상황을 기록하세요.")

    with st.form("add_book_form", clear_on_submit=True):
        name = st.text_input("책 제목", placeholder="예: 데미안")
        author = st.text_input("저자", placeholder="예: 헤르만 헤세")
        added_on = st.date_input("등록일", value=date.today())
        submitted = st.form_submit_button("책 추가", type="primary", use_container_width=True)
        if submitted:
            if name.strip() and author.strip():
                add_book(name, author, added_on)
                st.rerun()
            st.warning("책 제목과 저자를 모두 입력해 주세요.")

    st.divider()
    books: list[Book] = st.session_state.books
    render_summary(books)
    st.subheader("내 서재")
    render_book_list()
    st.subheader("월별 통계")
    render_monthly_statistics(books)


if __name__ == "__main__":
    main()