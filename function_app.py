import azure.functions as func
import logging
import json
import requests

app = func.FunctionApp()

@app.route(route="sanitize_rfs_form", auth_level=func.AuthLevel.FUNCTION)
def sanitize_rfs_form(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('RFS form received for HIPAA sanitization.')

    try:
        form_data = req.get_json()

        sanitized_data = {
            "first_name": form_data.get("patient_first_name"),
            "last_initial": form_data.get("patient_last_name", "")[:1],
            "dob": form_data.get("dob"),
            "reason": form_data.get("reason_for_seeking_services"),
            "modality": form_data.get("desired_modality")
        }

        webhook_url = "YOUR_POWER_AUTOMATE_WEBHOOK_URL"
        headers = {"Content-Type": "application/json"}

        response = requests.post(webhook_url, headers=headers, json=sanitized_data)

        if response.status_code == 200:
            return func.HttpResponse("Data sanitized and forwarded successfully.", status_code=200)
        else:
            logging.error("Middleware error: " + response.text)
            return func.HttpResponse("Middleware error: " + response.text, status_code=500)

    except Exception as e:
        logging.error("Exception occurred: " + str(e))
        return func.HttpResponse("Exception: " + str(e), status_code=500)
