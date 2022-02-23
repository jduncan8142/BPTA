import base64
import os
from jinja2 import Environment, FileSystemLoader
from Logger import LogProvider
from typing import Optional

class Reporter:
    def __init__(self, log_file: str, template_dir: Optional[str] = "Report_Templates", template: Optional[str] = "report_template.html", report_file: Optional[str] = "BPTA_Report.html") -> None:
        if type(log_file) is str:
            self.data = log_file
        else:
            raise TypeError(f"'log_file' must be a string for the file apth of the log file to report")
        self._report_file: str = os.path.join(os.getcwd(), "output", report_file)
        # Create a template Environment
        self.env = Environment(loader=FileSystemLoader(template_dir))
        # Load the template from the Environment
        self.template = self.env.get_template(template)
        self.html: str
        self.data: LogProvider
    
    def render_template(self) -> None:
        # Render the selected template with data variables provided
        self.html = self.template.render(
            page_title_text=self.data.page_title_text,
            title_text=self.data.title_text,

        )

    def generate_report(self, report_file: str, data: dict) -> str:
        #  Write the template to an HTML file
        with open(report_file, 'w') as f:
            f.write(self.html)
