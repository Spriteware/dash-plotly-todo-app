import uuid
import dash_mantine_components as dmc
from dash import Dash, _dash_renderer, dcc, ctx, html, Input, Output, State, ALL
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
_dash_renderer._set_react_version("18.2.0")  # for mantine


print("------- Loading app ------ ")

# Simplified to just one list
sample_list_data = [
    {
        "index": uuid.uuid4().hex,
        "title": "My Tasks",
        "tasks_list": [
            {
                "index": uuid.uuid4().hex,
                "content": "Task A", 
                "checked": True,
            },
            {
                "index": uuid.uuid4().hex,
                "content": "Task B", 
                "checked": False,
            },
            {
                "index": uuid.uuid4().hex,
                "content": "Task C", 
                "checked": False,
            },
        ],
    },
    {
        "index": uuid.uuid4().hex,
        "title": "Shopping list",
        "tasks_list": [],
    }
]


def get_task(task_dict):
    """ Returns a single task layout """
    text = task_dict["content"]
    checked = task_dict["checked"]
    index = task_dict["index"]

    content = dmc.Grid(
        [
            dmc.GridCol(
                dmc.Checkbox(
                    id={"type": "task_checked", "index": index},
                    checked=checked,
                    mt=2
                ), 
                span="content"
            ),
            dmc.GridCol(
                dmc.Text(
                    dcc.Input(
                        text, 
                        id={"type": "task_content", "index": index},
                        className="shadow-input",
                        debounce=True
                    )
                ), 
                span="auto"
            ),
            dmc.GridCol(
                dmc.ActionIcon(
                    DashIconify(icon="tabler:x", width=20),
                    id={"type": "task_del", "index": index},
                    variant="transparent",
                    color="gray",
                    className="task-del-button"
                ),
                span="content"
            ),
        ],
        className="task-container"
    )

    return content


def get_tasks_layout(tasks_list):
    """ Returns the list of tasks """
    tasks = []
    for task_dict in tasks_list:
        task_layout = get_task(task_dict)
        tasks.append(task_layout)

    return tasks


def get_list_layout():
    """ Returns the list of checkboxes """
    
    content = dmc.Paper(
        [
            dmc.Title(
                dcc.Input(
                    id="main_list_title", 
                    className="shadow-input",
                    debounce=True
                ),
                order=2
            ),
            
            dmc.Container(
                id="main_task_container",
                px=0,
                mt="md",
                mb="md",
            ),

            dmc.Group(
                [
                    dmc.Button(
                        "Add a new task", 
                        id="new_task_button",
                        #style={"width": "100%"},
                        variant="outline", 
                        color="gray",
                        mt="sm"
                    ),

                    dmc.Button(
                        "... or remove list",
                        id="del_list_button",
                        #style={"width": "100%"},
                        variant="subtle", 
                        color="red",
                        size="xs",
                        mt="sm"

                    )
                ]
            ),

            dmc.Modal(
                id="del_list_modal",
                title="Are you sure you want to delete this task list?",
                children=[
                    dmc.Group(
                        [
                            dmc.Button(
                                "Yes, delete", 
                                id="del_list_modal_confirm_button",
                                color="red"
                            ),
                        ],
                        justify="center",
                    ),
                ],
            ),
        ],
        shadow="sm",
        p="md",
        mt="md",
        radius="sm",
    )

    return content


def get_new_list_button():

    return dmc.Button(
        "New list",
        id="new_list_button",
        style={"width": "100%"},
        color="black",
        mt="md",
        mb="md"
    )


def get_list_navigation_layout(list_data, current_index):
    """ Returns a list of lists titles and progressions """

    items = []

    for list_item in list_data:

        # Compute progression
        progress_value = get_progression(list_item)
        progress_color = "green" if progress_value == 100 else "blue"

        # Build card element
        # We wraper the content with a A element to make it clickable (n_clicks)
        elem = dmc.Paper(
            html.A(
                [
                    dmc.Title(list_item["title"], order=4, mb="sm"),
                    dmc.Progress(value=progress_value, color=progress_color),
                ],
                id={"type": "list_button", "index": list_item["index"]},
                style={"cursor": "pointer"},
            ),
            p="xs",
            mb="sm",
            withBorder=True,
            className="active" if current_index == list_item["index"] else ""
        )

        items.append(elem)

    return items


def get_progression(list_item):
    """ Computes the progression of a list, returns 0 if tasks"""

    tasks = list_item["tasks_list"]
    if len(tasks) == 0:
        return 0

    return len([task for task in tasks if task["checked"]]) / len(tasks) * 100


def get_pos_from_index(dict_list, index):
    """ Retrives the current position in a list of dicts given an index """

    for i, elem in enumerate(dict_list):
        if elem["index"] == index:
            return i


app = Dash(__name__)

# Simplified app layout
app.layout = dmc.MantineProvider(
    [
        dmc.Container(
            dmc.Grid(
                [
                    dmc.GridCol(
                        [
                            get_new_list_button(),
                            dmc.Container(
                                id="list_navigation_layout",
                                px=0,
                            )
                        ],
                        span=4,
                    ),
                    dmc.GridCol(
                        get_list_layout(),
                        span="auto",
                        ml="xl"
                    ),
                ],
                gutter="md"
            ),
            size=600,
        ),
        dcc.Store("list_data_memory", data=sample_list_data, storage_type="local"),
        dcc.Store("current_index_memory", data=sample_list_data[0]["index"], storage_type="local"),
    ]
)

#################################### LISTS ###########################################


@app.callback(
    [
        Output("main_task_container", "children"),
        Output("main_list_title", "value"),
        Output("list_navigation_layout", "children"),
    ],
    [
        Input("list_data_memory", "data"),
        Input("current_index_memory", "data"),
    ]
)
def update_task_container(list_data, current_index):
    """ Updates the list of tasks and list title"""

    print("Entering update_task_container callback")
    
    # Get the current list 
    i = get_pos_from_index(list_data, current_index)
    curr_list = list_data[i]

    # Compute layout
    tasks_layout = get_tasks_layout(curr_list["tasks_list"])
    title_layout = curr_list["title"]
    list_navigation = get_list_navigation_layout(list_data, current_index)

    return tasks_layout, title_layout, list_navigation


@app.callback(
    Output("current_index_memory", "data", allow_duplicate=True),
    Input({"type": "list_button", "index": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def switch_list(n_clicks):
    """ Changes the current displayed list"""

    if not any(n_clicks):
        raise PreventUpdate

    list_index = ctx.triggered_id["index"]
    print(f"Switching list to `{list_index}`")
    return list_index


@app.callback(
    [
        Output("list_data_memory", "data", allow_duplicate=True),
        Output("current_index_memory", "data"),
    ],
    [
        Input("new_list_button", "n_clicks"),
        State("list_data_memory", "data"),
    ],
    prevent_initial_call=True,
)
def add_list(n_clicks, list_data):
    """ Add a new list and display it"""

    if not n_clicks:
        raise PreventUpdate

    print("Entering add_list callback")

    new_index = uuid.uuid4().hex
    new_list = {
        "index": new_index,
        "title": "New list",
        "tasks_list": [],
    }

    list_data.append(new_list)
    return list_data, new_index


@app.callback(
    Output("list_data_memory", "data", allow_duplicate=True),
    [
        Input("main_list_title", "value"),
        State("list_data_memory", "data"),
        State("current_index_memory", "data"),
    ],
    prevent_initial_call=True,
)
def update_list_title(title, list_data, current_index):
    """ Updates the current list title"""

    i = get_pos_from_index(list_data, current_index)
    list_data[i]["title"] = title
    return list_data


@app.callback(
    Output("del_list_modal", "opened"),
    [
        Input("del_list_button", "n_clicks"),
        Input("del_list_modal_confirm_button", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def delete_modal_open_close(n_clicks, n_clicks2):
    """ Open or closes modal. This could be clientside callback. """

    if not n_clicks:
        raise PreventUpdate

    # Close the modal after removing the list
    if ctx.triggered_id == "del_list_modal_confirm_button":
        return False

    return True


@app.callback(
    [
        Output("list_data_memory", "data", allow_duplicate=True),
        Output("current_index_memory", "data", allow_duplicate=True),
    ],
    [
        Input("del_list_modal_confirm_button", "n_clicks"),
        State("list_data_memory", "data"),
        State("current_index_memory", "data"),
    ],
    prevent_initial_call=True,
)
def delete_list(n_clicks, list_data, current_index):
    """ Updates the current list title """

    if not n_clicks:
        raise PreventUpdate

    # Remove the current list
    i = get_pos_from_index(list_data, current_index)
    del list_data[i]

    # Focus again on the first index if there are notes.
    current_index = list_data[0]["index"] if len(list_data) > 0 else None
    return list_data, current_index


#################################### TASKS ###########################################

@app.callback(
    Output("list_data_memory", "data", allow_duplicate=True),
    [
        Input("new_task_button", "n_clicks"),
        State("list_data_memory", "data"),
        State("current_index_memory", "data"),
    ],
    prevent_initial_call=True,
)
def add_task(n_clicks, list_data, current_index):
    """ Adds a task to the list """
    if not n_clicks:
        raise PreventUpdate

    print("Entering add_task callback")
    
    # Create new task dictionary
    new_index = uuid.uuid4().hex
    new_task = {
        "index": new_index,
        "content": "", 
        "checked": False,
    }
    
    # Add new task to the tasks list in memory
    i = get_pos_from_index(list_data, current_index)
    list_data[i]["tasks_list"].append(new_task)

    return list_data


@app.callback(
    Output("list_data_memory", "data", allow_duplicate=True),
    [
        Input({"type": "task_del", "index": ALL}, "n_clicks"),
        State("list_data_memory", "data"),
        State("current_index_memory", "data"),
    ],
    prevent_initial_call=True,
)
def remove_task(n_clicks, list_data, current_index):
    """ Remove a task from the list """
    if not any(n_clicks):
        raise PreventUpdate

    print("Entering remove_task callback")
    task_index = ctx.triggered_id["index"]

    # Find and remove the task with matching index
    i = get_pos_from_index(list_data, current_index)
    list_data[i]["tasks_list"] = [
        task for task in list_data[i]["tasks_list"] 
        if task["index"] != task_index
    ]
    
    return list_data


@app.callback(
    Output("list_data_memory", "data", allow_duplicate=True),
    [
        Input({"type": "task_checked", "index": ALL}, "checked"),
        Input({"type": "task_content", "index": ALL}, "value"),
        State("list_data_memory", "data"),
        State("current_index_memory", "data"),
    ],
    prevent_initial_call=True,
)
def update_task_checked(checked_values, content_values, list_data, current_index):
    """Updates the checked state of tasks"""
    if not checked_values:
        raise PreventUpdate
    
    print("Entering update_task_checked callback")

    i = get_pos_from_index(list_data, current_index)

    # Find the index position in our list of tasks
    task_index = ctx.triggered_id["index"]
    task_pos = get_pos_from_index(list_data[i]["tasks_list"], task_index)

    task_checked_value = checked_values[task_pos]
    task_content_value = content_values[task_pos]

    # Update the task values in list_data
    list_data[i]["tasks_list"][task_pos]["checked"] = task_checked_value
    list_data[i]["tasks_list"][task_pos]["content"] = task_content_value

    return list_data


if __name__ == '__main__':
    app.run_server(debug=True)
