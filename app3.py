import uuid
import dash_mantine_components as dmc
from dash import Dash, _dash_renderer, dcc, ctx, Input, Output, State, ALL
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
_dash_renderer._set_react_version("18.2.0")  # for mantine


print("------- Loading app ------ ")

# Simplified to just one list
sample_list_data = {
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
}


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
            dmc.Title(id="main_list_title", order=2),
            
            dmc.Container(
                id="main_task_container",
                px=0,
                mt="md",
                mb="md",
            ),

            dmc.Button(
                "Add a new task", 
                id="new_task_button",
                style={"width": "100%"},
                variant="outline", 
                color="gray",
            )
        ],
        shadow="sm",
        p="md",
        mt="md",
        radius="sm",
    )

    return content


app = Dash(__name__)

# Simplified app layout
app.layout = dmc.MantineProvider(
    [
        dmc.Container(
            get_list_layout(),
            size=400,
        ),
        dcc.Store("list_memory", data=sample_list_data, storage_type="local")
    ]
)


@app.callback(
    Output("main_task_container", "children"),
    Output("main_list_title", "children"),
    Input("list_memory", "data"),
)
def update_task_container(list_data):
    """ Updates the list of tasks and list title"""
    
    return get_tasks_layout(list_data["tasks_list"]), list_data["title"]


@app.callback(
    Output("list_memory", "data", allow_duplicate=True),
    Input("new_task_button", "n_clicks"),
    State("list_memory", "data"),
    prevent_initial_call=True,
)
def add_task(n_clicks, list_data):
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
    list_data["tasks_list"].append(new_task)
    return list_data


@app.callback(
    Output("list_memory", "data", allow_duplicate=True),
    Input({"type": "task_del", "index": ALL}, "n_clicks"),
    State("list_memory", "data"),
    prevent_initial_call=True,
)
def remove_task(n_clicks, list_data):
    """ Remove a task from the list """
    if not any(n_clicks):
        raise PreventUpdate

    print("Entering remove_task callback")
    task_index = ctx.triggered_id["index"]

    # Find and remove the task with matching index
    list_data["tasks_list"] = [
        task for task in list_data["tasks_list"] 
        if task["index"] != task_index
    ]
    
    return list_data


@app.callback(
    Output("list_memory", "data", allow_duplicate=True),
    Input({"type": "task_checked", "index": ALL}, "checked"),
    Input({"type": "task_content", "index": ALL}, "value"),
    State("list_memory", "data"),
    prevent_initial_call=True,
)
def update_task_checked(checked_values, content_values, list_data):
    """Updates the checked state of tasks"""
    if not checked_values:
        raise PreventUpdate
    
    print("Entering update_task_checked callback")

    # Find the index position in our list of tasks
    task_index = ctx.triggered_id["index"]
    task_pos = [task["index"] for task in list_data["tasks_list"]].index(task_index)

    task_checked_value = checked_values[task_pos]
    task_content_value = content_values[task_pos]

    # Update the task values in list_data
    list_data["tasks_list"][task_pos]["checked"] = task_checked_value
    list_data["tasks_list"][task_pos]["content"] = task_content_value

    return list_data


if __name__ == '__main__':
    app.run_server(debug=True)