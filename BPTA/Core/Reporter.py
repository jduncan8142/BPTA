import base64
import logging
import os
from jinja2 import Environment, FileSystemLoader
from typing import Optional

class Reporter:
    def __init__(self, data: dict, template_dir: Optional[str] = "Report_Templates", template: Optional[str] = "report_template.html") -> None:
        if type(data) is dict:
            self.data = data
        else:
            raise TypeError(f"'data' must be of type <dict> but got type {type(data)}")
        # Create a template Environment
        self.env = Environment(loader=FileSystemLoader(template_dir))
        # Load the template from the Environment
        self.template = self.env.get_template(template)
        # Render the selected template with data variables provided
        self.html: str = template.render(
            page_title_text=self.data.page_title_text,
            title_text=self.data.title_text,
        )

    def generate_report(self, report_file: str, data: dict) -> str:
        #  Write the template to an HTML file
        with open(report_file, 'w') as f:
            f.write(self.html)
