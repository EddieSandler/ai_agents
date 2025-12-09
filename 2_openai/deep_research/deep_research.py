import importlib

try:
    gr = importlib.import_module("gradio")
except ImportError as exc:
    gr = None
    _gradio_import_error = exc
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)


async def run(query: str):
    async for chunk in ResearchManager().run(query):
        yield chunk


if gr is None:
    raise RuntimeError(
        "gradio is required to launch the UI. "
        "Install it with `pip install gradio` in the project environment."
    ) from _gradio_import_error

with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research")
    query_textbox = gr.Textbox(label="What topic would you like to research?")
    run_button = gr.Button("Run", variant="primary")
    report = gr.Markdown(label="Report")

    run_button.click(fn=run, inputs=query_textbox, outputs=report)
    query_textbox.submit(fn=run, inputs=query_textbox, outputs=report)

ui.launch(inbrowser=True)

