"""
SOC Report Authoring Tool
------------------------
A Streamlit-based web application for generating SOC monthly reports with PDF export capabilities.

This tool allows users to:
- Create and edit SOC monthly reports with a user-friendly interface
- Import/Export report data in JSON format
- Generate PDF reports using customizable templates
- Preview reports in real-time
- Manage multiple cyberattack entries and threat levels

Dependencies:
    - streamlit
    - jinja2
    - playwright
    - json
    - ssl

Author: https://github.com/thomasboegl1
Version: 1.0.0
"""

import streamlit as st
from jinja2 import Template
import json
import ssl
from playwright.sync_api import sync_playwright


class SOCReportAuthoringTool:
    """
    Main class for the SOC Report Authoring Tool.

    This class handles all the functionality for creating, editing, and exporting
    SOC monthly reports through a Streamlit web interface.
    """

    def __init__(self):
        """
        Initialize the SOC Report Authoring Tool.

        Sets up the Streamlit page configuration and loads the HTML template.
        Initializes session state if not already present.
        """
        # Load template from external file
        self.template_path = "threat-report.html"
        with open(self.template_path, 'r') as file:
            self.template = file.read()

        # Configure Streamlit page settings
        st.set_page_config(
            page_title="SOC Monthly Report Authoring Tool",
            page_icon="🛡️",
            layout="wide"
        )

        # Initialize session state if needed
        if 'form_data' not in st.session_state:
            st.session_state.form_data = self.get_default_form_data()

    def get_default_form_data(self):
        """
        Get default form data structure.

        Returns:
            dict: Default form data with empty values for all fields.
        """
        return {
            "report_date": "",
            "threat_level": "Guarded",
            "generalSituation": "",
            "hunting_text": "",
            "attack1": {
                "title": "",
                "image": "",
                "description": "",
                "mitigated": False
            },
            "attack2": {
                "title": "",
                "image": "",
                "description": "",
                "mitigated": False
            },
            "attack3": {
                "title": "",
                "image": "",
                "description": "",
                "mitigated": False
            },
            "takeaway": {
                "quote": "",
                "author": "",
                "picture": ""
            }
        }

    def update_field(self, field_path: str, value: any) -> None:
        """
        Update a nested field in form_data using dot notation.

        Args:
            field_path (str): Path to the field using dot notation (e.g., 'attack1.title')
            value (any): New value to set for the field
        """
        data = st.session_state.form_data
        parts = field_path.split('.')

        # Navigate to the correct nested level
        for part in parts[:-1]:
            data = data[part]

        # Update the value
        data[parts[-1]] = value

    def get_field_value(self, field_path: str) -> any:
        """
        Get a nested field value from form_data using dot notation.

        Args:
            field_path (str): Path to the field using dot notation

        Returns:
            any: Value of the specified field
        """
        data = st.session_state.form_data
        for part in field_path.split('.'):
            data = data[part]
        return data

    def get_field_values(self) -> dict:
        """
        Get all current form values.

        Returns:
            dict: Current state of all form fields
        """
        return st.session_state.form_data

    def import_json(self, json_data: dict) -> None:
        """
        Import JSON data into session state.

        Args:
            json_data (dict): JSON data to import
        """
        st.session_state.form_data = json_data

    def render_template(self, field_values: dict) -> str:
        """
        Render the HTML template with provided field values.

        Args:
            field_values (dict): Values to use in template rendering

        Returns:
            str: Rendered HTML content or None if error occurs
        """
        try:
            template = Template(self.template)
            return template.render(**field_values)
        except Exception as e:
            st.error(f"Error rendering template: {e}")
            return None

    def generate_pdf(self, html_content: str) -> bytes:
        """
        Generate a PDF from HTML content using Playwright.

        Args:
            html_content (str): HTML content to convert to PDF

        Returns:
            bytes: PDF file content or None if error occurs
        """
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()

                # Set the HTML content and wait until all network requests are done
                page.set_content(html_content)

                # Generate the PDF with specific formatting options
                pdf_bytes = page.pdf(format="A4", print_background=True, scale=0.60)

                browser.close()
                return pdf_bytes
        except Exception as e:
            st.error(f"Error generating PDF: {e}")
            return None

    def run(self) -> None:
        """
        Run the Streamlit application.

        This method sets up the UI layout and handles all user interactions.
        """
        # Main title
        st.title("🛡️ SOC Monthly Report Generator")

        # Top bar with action buttons
        col1, col2, col3 = st.columns([1, 1, 1])

        # PDF generation and export buttons
        with col1:
            if st.button("Generate PDF", type="primary"):
                rendered_html = self.render_template(self.get_field_values())
                if rendered_html:
                    pdf_bytes = self.generate_pdf(rendered_html)
                    if pdf_bytes:
                        st.download_button(
                            label="Download PDF",
                            data=pdf_bytes,
                            file_name=f"SOC_Report_{st.session_state.form_data['report_date'].replace(' ', '_')}.pdf",
                            mime="application/pdf"
                        )
            st.download_button(
                label="Export JSON",
                data=json.dumps(self.get_field_values(), indent=2),
                file_name=f"SOC_Report_{st.session_state.form_data['report_date'].replace(' ', '_')}.json",
                mime="application/json",
            )

        # JSON import functionality
        with col2:
            uploaded_file = st.file_uploader("Import JSON", type="json")
            if uploaded_file is not None and 'last_uploaded_file' not in st.session_state:
                try:
                    data = json.loads(uploaded_file.getvalue())
                    self.import_json(data)
                    st.session_state.last_uploaded_file = uploaded_file.name
                    st.success("Data imported successfully!")
                except Exception as e:
                    st.error(f"Error importing JSON: {e}")
            elif uploaded_file is None:
                if 'last_uploaded_file' in st.session_state:
                    del st.session_state.last_uploaded_file

        # Main content area
        input_col, preview_col = st.columns([1, 2])

        # Input form
        with input_col:
            st.header("Report Details")

            # Basic report information
            st.text_input(
                "Report Month",
                value=self.get_field_value("report_date"),
                key="report_date_input",
                on_change=lambda: self.update_field("report_date", st.session_state.report_date_input)
            )

            st.selectbox(
                "Threat Level",
                ["Guarded", "Elevated", "High", "Severe"],
                index=["Guarded", "Elevated", "High", "Severe"].index(self.get_field_value("threat_level")),
                key="threat_level_input",
                on_change=lambda: self.update_field("threat_level", st.session_state.threat_level_input)
            )

            # Detailed report sections
            st.text_area(
                "General Situation",
                value=self.get_field_value("generalSituation"),
                height=150,
                key="general_situation_input",
                on_change=lambda: self.update_field("generalSituation", st.session_state.general_situation_input)
            )

            st.text_area(
                "Hunting Details",
                value=self.get_field_value("hunting_text"),
                height=150,
                key="hunting_text_input",
                on_change=lambda: self.update_field("hunting_text", st.session_state.hunting_text_input)
            )

            # Cyberattack entries
            st.subheader("Recent Cyberattacks")

            # Attack entry fields (1-3)
            for i in range(1, 4):
                attack_key = f"attack{i}"
                st.markdown(f"#### Attack {i}")

                # Attack details form fields
                st.text_input(
                    f"Attack {i} Title",
                    value=self.get_field_value(f"{attack_key}.title"),
                    key=f"{attack_key}_title_input",
                    on_change=lambda k=attack_key: self.update_field(f"{k}.title",
                        st.session_state[f"{k}_title_input"])
                )

                st.text_input(
                    f"Attack {i} Image URL",
                    value=self.get_field_value(f"{attack_key}.image"),
                    key=f"{attack_key}_image_input",
                    on_change=lambda k=attack_key: self.update_field(f"{k}.image",
                        st.session_state[f"{k}_image_input"])
                )

                st.text_area(
                    f"Attack {i} Description",
                    value=self.get_field_value(f"{attack_key}.description"),
                    height=100,
                    key=f"{attack_key}_description_input",
                    on_change=lambda k=attack_key: self.update_field(f"{k}.description",
                        st.session_state[f"{k}_description_input"])
                )

                st.checkbox(
                    "Mitigated by SOC",
                    value=self.get_field_value(f"{attack_key}.mitigated"),
                    key=f"{attack_key}_mitigated_input",
                    on_change=lambda k=attack_key: self.update_field(f"{k}.mitigated",
                        st.session_state[f"{k}_mitigated_input"])
                )

            # Takeaway section
            st.subheader("Take Away")
            st.text_area(
                "Quote",
                value=self.get_field_value("takeaway.quote"),
                height=100,
                key="takeaway_quote_input",
                on_change=lambda: self.update_field("takeaway.quote", st.session_state.takeaway_quote_input)
            )

            st.text_input(
                "Author",
                value=self.get_field_value("takeaway.author"),
                key="takeaway_author_input",
                on_change=lambda: self.update_field("takeaway.author", st.session_state.takeaway_author_input)
            )

            st.text_input(
                "Author Image URL",
                value=self.get_field_value("takeaway.picture"),
                key="takeaway_picture_input",
                on_change=lambda: self.update_field("takeaway.picture", st.session_state.takeaway_picture_input)
            )

        # Live preview
        with preview_col:
            st.header("Live Preview")
            rendered_html = self.render_template(self.get_field_values())
            if rendered_html:
                st.components.v1.html(rendered_html, height=2000, scrolling=True)


def main():
    """
    Main entry point for the application.

    Sets up SSL context and initializes the SOC Report Authoring Tool.
    """
    # Configure SSL context for HTTPS requests
    ssl._create_default_https_context = ssl._create_unverified_context

    # Initialize and run the tool
    tool = SOCReportAuthoringTool()
    tool.run()


if __name__ == "__main__":
    main()
