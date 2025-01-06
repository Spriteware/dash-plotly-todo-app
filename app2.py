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


def get_list_layout(list_data):
    """ Returns the list of checkboxes """

    tasks_layout = get_tasks_layout(list_data["tasks_list"])

    content = dmc.Paper(
        [
            dmc.Title(list_data["title"], order=2),
            
            dmc.Container(
                tasks_layout,
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
    dmc.Container(
        get_list_layout(sample_list_data),
        size=400,
    )
)


@app.callback(
    Output("main_task_container", "children", allow_duplicate=True),
    Input("new_task_button", "n_clicks"),
    State("main_task_container", "children"),
    prevent_initial_call=True,
)
def add_task(n_clicks, current_tasks):
    """ Adds a task to the list """
    if not n_clicks:
        raise PreventUpdate

    print("Entering add_task callback")

    new_index = uuid.uuid4().hex
    task_dict = {
        "index": new_index,
        "content": "", 
        "checked": False,
    }
    task_layout = get_task(task_dict)
    
    # Add new task to current tasks
    updated_tasks = current_tasks + [task_layout]
    return updated_tasks


@app.callback(
    Output("main_task_container", "children", allow_duplicate=True),
    Input({"type": "task_del", "index": ALL}, "n_clicks"),
    State("main_task_container", "children"),
    prevent_initial_call=True,
)
def remove_task(n_clicks, current_tasks):
    """ Remove a task from the list """
    if not any(n_clicks):
        raise PreventUpdate

    print("Entering remove_task callback")
    task_index = ctx.triggered_id["index"]

    # Get the list of existing ids.
    all_ids = [elem["id"] for elem in ctx.inputs_list[0]]

    # Find the position of element in list and remove it
    for i, task_id in enumerate(all_ids):
        if task_id["index"] == task_index:
            del current_tasks[i]
            break 

    return current_tasks


if __name__ == '__main__':
    app.run_server(debug=True)