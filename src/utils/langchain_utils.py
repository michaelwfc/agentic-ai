from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph


def save_graph_as_markdown(graph: CompiledStateGraph, filename="graph.md"):
    """Save graph as Markdown file with Mermaid diagram for VS Code preview"""
    mermaid_code = graph.get_graph().draw_mermaid()

    markdown_content = f"""# LangGraph Diagram

```mermaid
{mermaid_code}
```
"""

    with open(filename, "w") as f:
        f.write(markdown_content)
    print(f"Graph saved as '{filename}' - VS Code will render the Mermaid diagram automatically")



def save_graph_image(graph:CompiledStateGraph,filename="graph.png",graph_dir="./images/langgraph_images"):
    # View
    # display(Image(graph.get_graph().draw_mermaid_png()))

    # View - Save PNG to file for VS Code
    png_data = graph.get_graph().draw_mermaid_png()
    filepath = f"{graph_dir}/{filename}"
    with open(filepath, "wb") as f:
      f.write(png_data)
    print(f"Graph saved as '{filename}' - open this file in VS Code to view")

    # Alternative: Get Mermaid markup (VS Code can render this)
    # mermaid_code = graph.get_graph().draw_mermaid()
    # print("\nMermaid code (copy to a .md file with ```mermaid):")
    # print(mermaid_code)

    # Save as Markdown file (recommended for VS Code)
    # save_graph_as_markdown(graph)