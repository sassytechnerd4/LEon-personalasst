from bridges.python.src.sdk.memory import Memory
from typing import TypedDict, Optional

from datetime import datetime


todo_lists_memory = Memory({
    'name': 'todo_lists',
    'default_memory': []
})

todo_items_memory = Memory({
    'name': 'todo_items',
    'default_memory': []
})


class TodoListMemory(TypedDict):
    widget_id: str
    name: str
    created_at: str
    updated_at: str


class TodoItemMemory(TypedDict):
    widget_id: str
    todo_list_name: str
    name: str
    is_completed: bool
    created_at: str
    updated_at: str


def create_todo_list(widget_id: Optional[str], name: str) -> None:
    """Create a new todo list"""

    datetime_now = datetime.now().isoformat()
    todo_list = TodoListMemory(
        widget_id=widget_id,
        name=name,
        created_at=datetime_now,
        updated_at=datetime_now
    )
    todo_lists: list[TodoListMemory] = todo_lists_memory.read()
    todo_lists.append(todo_list)
    todo_lists_memory.write(todo_lists)

def get_todo_list_by_name(name: str) -> TodoListMemory:
    """Get a todo list by name"""

    todo_lists: list[TodoListMemory] = todo_lists_memory.read()
    for todo_list in todo_lists:
        if todo_list['name'] == name:
            return todo_list

    return None

def get_todo_list_by_widget_id(widget_id: str) -> TodoListMemory:
    """Get a todo list by widget id"""

    todo_lists: list[TodoListMemory] = todo_lists_memory.read()
    for todo_list in todo_lists:
        if todo_list['widget_id'] == widget_id:
            return todo_list

    return None


def get_todo_lists() -> list[TodoListMemory]:
    """Get all todo lists"""

    return todo_lists_memory.read()


def update_todo_list(old_name: str, new_name: str) -> None:
    """Update a todo list name"""

    todo_lists: list[TodoListMemory] = todo_lists_memory.read()
    for todo_list in todo_lists:
        if todo_list['name'] == old_name:
            todo_list['name'] = new_name
            todo_list['updated_at'] = datetime.now().isoformat()
            break
    todo_lists_memory.write(todo_lists)

    todo_items: list[TodoItemMemory] = todo_items_memory.read()
    for todo_item in todo_items:
        if todo_item['todo_list_name'] == old_name:
            todo_item['todo_list_name'] = new_name
            todo_item['updated_at'] = datetime.now().isoformat()
    todo_items_memory.write(todo_items)


def delete_todo_list(name: str) -> None:
    """Delete a todo list and its todos"""

    todo_lists: list[TodoListMemory] = todo_lists_memory.read()
    for todo_list in todo_lists:
        if todo_list['name'] == name:
            todo_lists.remove(todo_list)
            break
    todo_lists_memory.write(todo_lists)

    todo_items: list[TodoItemMemory] = todo_items_memory.read()
    for todo_item in todo_items:
        if todo_item['todo_list_name'] == name:
            todo_items.remove(todo_item)
    todo_items_memory.write(todo_items)


def count_todo_lists() -> int:
    """Count the number of todo lists"""

    return len(todo_lists_memory.read())


def has_todo_list(name: str) -> bool:
    """Check if a todo list already exist"""

    todo_lists: list[TodoListMemory] = todo_lists_memory.read()
    for todo_list in todo_lists:
        if todo_list['name'] == name:
            return True
    return False


def create_todo_item(widget_id: str, todo_list_name: str, name: str) -> None:
    """Create a new todo item"""

    if not has_todo_list(todo_list_name):
        create_todo_list(widget_id, todo_list_name)

    datetime_now = datetime.now().isoformat()
    todo_item = TodoItemMemory(
        widget_id=widget_id,
        todo_list_name=todo_list_name,
        name=name,
        is_completed=False,
        created_at=datetime_now,
        updated_at=datetime_now
    )
    todo_items: list[TodoItemMemory] = todo_items_memory.read()
    todo_items.append(todo_item)
    todo_items_memory.write(todo_items)


def get_todo_items(widget_id: Optional[str], todo_list_name: str) -> list[TodoItemMemory]:
    """Get all todo items of a todo list"""

    todo_items: list[TodoItemMemory] = todo_items_memory.read()

    if widget_id is not None:
        return [todo_item for todo_item in todo_items if todo_item['todo_list_name'] == todo_list_name and todo_item['widget_id'] == widget_id]

    return [todo_item for todo_item in todo_items if todo_item['todo_list_name'] == todo_list_name]


def count_todo_items(todo_list_name: str) -> int:
    """Count the number of todo items of a todo list"""

    return len(get_todo_items(todo_list_name))


def get_completed_todo_items(todo_list_name: str) -> list[TodoItemMemory]:
    """Get all completed todo items of a todo list"""

    todo_items: list[TodoItemMemory] = todo_items_memory.read()
    return [todo_item for todo_item in todo_items if todo_item['todo_list_name'] == todo_list_name and todo_item['is_completed']]


def get_uncompleted_todo_items(todo_list_name: str) -> list[TodoItemMemory]:
    """Get all uncompleted todo items of a todo list"""

    todo_items: list[TodoItemMemory] = todo_items_memory.read()
    return [todo_item for todo_item in todo_items if todo_item['todo_list_name'] == todo_list_name and not todo_item['is_completed']]


def toggle_todo_item(todo_list_name: str, name: str) -> None:
    """Toggle a todo item"""

    todo_items: list[TodoItemMemory] = todo_items_memory.read()
    for todo_item in todo_items:
        if todo_item['todo_list_name'] == todo_list_name and todo_item['name'] == name:
            todo_item['is_completed'] = not todo_item['is_completed']
            todo_item['updated_at'] = datetime.now().isoformat()
            break
    todo_items_memory.write(todo_items)

def complete_todo_item(todo_list_name: str, name: str) -> None:
    """Complete a todo item"""

    todo_items: list[TodoItemMemory] = todo_items_memory.read()
    for todo_item in todo_items:
        if todo_item['todo_list_name'] == todo_list_name and todo_item['name'] == name:
            todo_item['is_completed'] = True
            todo_item['updated_at'] = datetime.now().isoformat()
            break
    todo_items_memory.write(todo_items)


def uncomplete_todo_item(todo_list_name: str, name: str) -> None:
    """Uncomplete a todo item"""

    todo_items: list[TodoItemMemory] = todo_items_memory.read()
    for todo_item in todo_items:
        if todo_item['todo_list_name'] == todo_list_name and todo_item['name'] == name:
            todo_item['is_completed'] = False
            todo_item['updated_at'] = datetime.now().isoformat()
            break
    todo_items_memory.write(todo_items)
