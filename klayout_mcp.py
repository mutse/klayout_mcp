import klayout
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("klayout_mcp")
current_layout = None

@mcp.tool()
def load_layout(file_path: str):
    global current_layout
    current_layout = klayout.db_layout()
    current_layout.read(file_path)
    return f"Loaded layout from {file_path}"

@mcp.tool()
def create_cell(cell_name: str):
    global current_layout
    if current_layout is None:
        raise ValueError("No layout loaded")
    cell = current_layout.create_cell(cell_name)
    return f"Created cell {cell_name}"

@mcp.tool()
def draw_rectangle(layer_num: int, datatype: int, x1: float, y1: float, x2: float, y2: float):
    global current_layout
    if current_layout is None:
        raise ValueError("No layout loaded")
    layer = klayout.db_layer(layer_num, datatype)
    cell = current_layout.top_cell()
    if cell is None:
        raise ValueError("No top cell")
    shape = cell.insert(klayout.db_shape(layer, klayout.db_box(x1, y1, x2, y2)))
    return f"Draw rectangle on layer {layer_num}/{datatype} from ({x1}, {y1}) to ({x2}, {y2})"

@mcp.tool()
def save_layout(file_path: str):
    global current_layout
    if current_layout is None:
        raise ValueError("No layout loaded")
    current_layout.write(file_path)
    return f"Saved layout to {file_path}"

if __name__ == "__main__":
    mcp.run(transport='stdio')
