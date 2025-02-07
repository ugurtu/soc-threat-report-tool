# SOC Report Authoring Tool 🛡️

A streamlined web application built with Streamlit for Security Operations Center (SOC) teams to create, manage, and export professional monthly security reports. Generate consistent, well-formatted PDF reports with customizable templates and real-time preview capabilities.

## Features

- 📝 User-friendly interface for creating and editing SOC monthly reports
- 🔄 Real-time preview of the report as you type
- 💾 Import/Export report data in JSON format
- 📄 Generate professional PDF reports using customizable templates
- 🎨 Clean, modern interface with responsive design

## Demo

You can find a sample report generated using the tool [here](samples/SOC_Report_January_2025.pdf). and a sameple json file [here](samples/SOC_Report_January_2025.json).

The report template is fully customizable and can be tailored to your organization's specific requirements.
I really suggest to change the template to fit your needs as I did not invest a lot of time in the generic one.

## Installation

```bash
# Clone the repository
git clone https://github.com/thomasboegl1/soc-threat-report-tool.git
cd soc-threat-report-tool

# Create and activate virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Access the web interface at `http://localhost:8501`

3. Fill in the report details:
   - Set report month and threat level
   - Add general situation assessment
   - Document recent cyberattacks
   - Include hunting details
   - Add takeaway quote and author

4. Use the live preview to verify the report layout
5. Export as PDF or JSON when finished

## Dependencies

- streamlit
- jinja2
- playwright
- json
- ssl

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Created by [thomasboegl1](https://github.com/thomasboegl1)
- Built with [Streamlit](https://streamlit.io/)
