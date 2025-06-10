import streamlit as st
import requests
import json

st.title("LeadGen Email Assistant")

# Initialize session state
if 'generated_template' not in st.session_state:
    st.session_state.generated_template = None
if 'form_data' not in st.session_state:
    st.session_state.form_data = {
        "company_name": "",
        "contact_name": "",
        "industry": "",
        "purpose": ""
    }

# Input form
st.header("Input Lead Details")
st.session_state.form_data["company_name"] = st.text_input("Company Name", value=st.session_state.form_data["company_name"])
st.session_state.form_data["contact_name"] = st.text_input("Contact Name", value=st.session_state.form_data["contact_name"])
st.session_state.form_data["industry"] = st.text_input("Industry", value=st.session_state.form_data["industry"])
st.session_state.form_data["purpose"] = st.text_input("Email Purpose", value=st.session_state.form_data["purpose"])

if st.button("Generate Template"):
    if all(st.session_state.form_data.values()):
        try:
            response = requests.post("http://localhost:8000/generate_template", json={
                "company_name": st.session_state.form_data["company_name"],
                "contact_name": st.session_state.form_data["contact_name"],
                "industry": st.session_state.form_data["industry"],
                "purpose": st.session_state.form_data["purpose"]
            })
            response.raise_for_status()
            st.session_state.generated_template = response.json()
            st.success("Template generated successfully!")
        except requests.exceptions.HTTPError as e:
            st.error(f"Error generating template: {str(e)}")
            if e.response.status_code == 422:
                st.error(f"Details: {e.response.json().get('detail', 'Invalid input')}")
        except Exception as e:
            st.error(f"Error generating template: {str(e)}")
    else:
        st.error("Please fill all fields.")

# Display template and save option
if st.session_state.generated_template:
    st.header("Generated Template")
    st.write(f"**Subject**: {st.session_state.generated_template['subject']}")
    st.write(f"**Body**: {st.session_state.generated_template['body']}")

    if st.button("Save Lead and Template"):
        if not all([st.session_state.form_data["company_name"], 
                    st.session_state.form_data["contact_name"], 
                    st.session_state.form_data["industry"]]):
            st.error("Please ensure all lead fields are filled.")
        elif not st.session_state.generated_template:
            st.error("No template available to save. Please generate a template first.")
        else:
            try:
                # Create lead
                lead_data = {
                    "company_name": st.session_state.form_data["company_name"],
                    "contact_name": st.session_state.form_data["contact_name"],
                    "industry": st.session_state.form_data["industry"]
                }
                st.write(f"Debug: Sending lead_data to http://localhost:8000/leads: {json.dumps(lead_data, indent=2)}")
                # Try with local_kw as a fallback
                lead_response = requests.post(
                    "http://localhost:8000/leads?local_kw=dummy",
                    json=lead_data,
                    headers={"Content-Type": "application/json"}
                )
                lead_response.raise_for_status()
                lead = lead_response.json()
                lead_id = lead['id']

                # Create template
                template_data = {
                    "lead_id": lead_id,
                    "subject": st.session_state.generated_template['subject'],
                    "body": st.session_state.generated_template['body']
                }
                st.write(f"Debug: Sending template_data to http://localhost:8000/templates: {json.dumps(template_data, indent=2)}")
                template_response = requests.post(
                    "http://localhost:8000/templates",
                    json=template_data,
                    headers={"Content-Type": "application/json"}
                )
                template_response.raise_for_status()
                template = template_response.json()
                st.success(f"Lead and Template saved successfully! Lead ID: {lead_id}, Template ID: {template['id']}")
                st.session_state.generated_template = None
            except requests.exceptions.HTTPError as e:
                st.error(f"Error saving lead or template: {str(e)}")
                if e.response.status_code == 422:
                    st.error(f"Details: {e.response.json().get('detail', 'Invalid input')}")
                # st.write(f"Debug: Request URL: {e.request.url}")
                # st.write(f"Debug: Request Body: {e.request.body.decode('utf-8')}")
            except Exception as e:
                st.error(f"Error saving lead or template: {str(e)}")