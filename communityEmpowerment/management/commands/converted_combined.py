import json
from datetime import datetime
import re
import os

# base_file_path = "/Users/gangadgaryadav/iitroorkeebackend/backend-roorkee/communityEmpowerment/management/scrapedData"
base_file_path = os.path.join(os.path.dirname(__file__), '..','scrapedData')

def remove_leading_numbers(title):
    # Use a regular expression to remove leading numbers followed by a dot and whitespace
    return re.sub(r'^\d+\.\s*', '', title)
# Helper function to convert date format
def convert_date_format(date_str):
    if date_str:
        try:
            return datetime.strptime(date_str, "%d %b %Y").strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            return None
    return None

# Helper function to determine tags based on scheme title and description
def determine_tags(title, description):
    tags = []
    text = f"{title} {description}".lower()
    if "scholarship" in text:
        tags.append("scholarship")
    if "job" in text or "employment" in text:
        tags.append("job")
    return tags

def transform_and_add_meghalaya_data(original_data, combined_data):
    for item in original_data:
        state_name = "Meghalaya"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)

# Function to transform and add Tamil Nadu data
def transform_and_add_tamilnadu_data(original_data, combined_data):
    for item in original_data:
        state_name = "Tamil Nadu"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("Concerned Department").strip()
        organisation_name = item.get("Organisation Name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": organisation_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = item.get("Title / Name").strip()
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("Introduced On")),
            "valid_upto": "2024-12-31T23:59:59Z",
            "funding_pattern": item.get("Sponsored By"),
            "description": description,
            "scheme_link": item.get("URL"),
            "beneficiaries": [
                {"beneficiary_type": item.get("Beneficiaries")}
            ] if item.get("Beneficiaries") else [],
            "documents": [],
            "sponsors": [
                {"sponsor_type": item.get("Sponsored By")}
            ],
            "criteria": [
                {"description": item.get("How To Avail"), "value": ""}
            ] if item.get("How To Avail") else [],
            "procedures": [
                {"step_description": item.get("How To Avail")}
            ] if item.get("How To Avail") else [],
            "tags": determine_tags(title, description)
        }
        organisation["schemes"].append(scheme)

# Function to transform and add Puducherry data
def transform_and_add_puducherry_data(original_data, combined_data):
    for item in original_data:
        state_name = "Puducherry"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)

# Function to transform and add Jammu and Kashmir data
def transform_and_add_jammukashmir_data(original_data, combined_data):
    for item in original_data:
        state_name = "Jammu and Kashmir"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)

def transform_and_add_gujarat_data(original_data, combined_data):
    for item in original_data:
        state_name = "Gujarat"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags",[])
        }
        organisation["schemes"].append(scheme)
    

def transform_and_add_maharashtra_data(original_data, combined_data):
    for item in original_data:
        state_name = "Maharashtra"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)


def transform_and_add_uttar_pradesh_data(original_data, combined_data):
    for item in original_data:
        state_name = "Uttar Pradesh"
        created_at = "2024-06-25T12:00:00Z"
        department_name = "उत्तर प्रदेश सरकार"
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        scheme_link = item.get("scheme_link")
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": convert_date_format(item.get("valid_upto")),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": scheme_link,
            
            "beneficiaries": [
                {"beneficiary_type": beneficiary} for beneficiary in item.get("beneficiaries", [])
            ],
            "sponsors": [
                {"sponsor_type": sponsor} for sponsor in item.get("sponsors", [])
            ],
            "criteria": [
                {"description": criterion, "value": ""} for criterion in item.get("criteria", [])
            ],
            "procedures": [
                {"step_description": step} for step in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description),
            "benefits": [
                {"benefit_type": benefit} for benefit in item.get("benefits", [])
            ],
            "criteria": [
                {"description": eligibility} for eligibility in item.get("eligibility", [])
            ],
            "application_process": [
                {"step_description": step} for step in item.get("application_process", [])
            ],
            "documents": [
                {"document_name": requirement} for requirement in item.get("requirements", [])
            ]
        }
        organisation["schemes"].append(scheme)

def transform_and_add_himachal_pradesh_data(original_data, combined_data):
    for item in original_data:
        state_name = "Himachal Pradesh"
        created_at = "2024-06-25T12:00:00Z"
        department_name = "other"
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("name").strip())
        description = item.get("objective")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("Introduced on: ")),
            "valid_upto": "2024-12-31T23:59:59Z",
            "funding_pattern": item.get("Sponsors: "),
            "description": description,
            "scheme_link": item.get("applyOnlineLink"),
            "beneficiaries": [
                {"beneficiary_type": item.get("Scheme Beneficiaries: ").strip()}
            ] if item.get("Scheme Beneficiaries: ") else [],
            "documents": [],
            "sponsors": [
                {"sponsor_type": item.get("Sponsors: ")}
            ],
            "criteria": [
                {"description": item.get("eligibility")}
                ],
            "procedures": [
                {"step_description": item.get("process")}
                ],
            "tags": determine_tags(title, description)
        }
        organisation["schemes"].append(scheme)

def transform_and_add_manipur_data(original_data, combined_data):
    for item in original_data:
        state_name = "Manipur"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)

def transform_and_add_kerela_data(original_data, combined_data):
    for item in original_data:
        state_name = "Kerala"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)

def transform_and_add_madhya_pradesh_data(original_data, combined_data):
    for item in original_data:
        state_name = "Madhya Pradesh"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)


def transform_and_add_kerela_data(original_data, combined_data):
    for item in original_data:
        state_name = "Kerala"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)

def transform_and_add_goa_data(original_data, combined_data):
    state_name = "Goa"

    for item in original_data:
        title = remove_leading_numbers(item.get("title", "").strip())


        state = {
            "state_name": state_name,
            "departments": []
        }
        combined_data["states"].append(state)

        department_name = item.get("department_name", "").strip()


        department = {
            "department_name": department_name,
            "organisations": [
                {
                    "organisation_name": department_name,
                    "schemes": []
                }
            ]
        }
        state["departments"].append(department)

        organisation = department["organisations"][0]
        description = item.get("description", "").strip()

        scheme = {
            "title": title,
            "introduced_on": item.get("introduced_on","").strip(),
            "valid_upto": None if item.get("valid_upto", "").strip() == "" else item["valid_upto"].strip(),
            "funding_pattern": item.get("funding_pattern", "").strip(),
            "description": description,
            "scheme_link": item.get("schemeUrl"),
            "pdf_url": item.get("pdfUrl"),
            "beneficiaries": [
                {"beneficiary_type": item.get("beneficiary", "").strip()}
            ],
            "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ], 
            "sponsors": [],  
            "criteria": item.get("criteria",""),
            "procedures": item.get("procedures",""),
            "benefits": [
                {"benefit_type": item.get("benefits", [])} 
            ],
            "tags": item.get("tags"),  # Implement determine_tags function
            "statistical_summary": []  # Exclude 'year' field from statistical summary
        }
        organisation["schemes"].append(scheme)

def transform_and_add_jharkhand_data(original_data, combined_data):
    state_name = "Jharkhand"

    for item in original_data:
        title = remove_leading_numbers(item.get("title", "").strip())


        state = {
            "state_name": state_name,
            "departments": []
        }
        combined_data["states"].append(state)

        department_name = item.get("department_name", "").strip()


        department = {
            "department_name": department_name,
            "organisations": [
                {
                    "organisation_name": department_name,
                    "schemes": []
                }
            ]
        }
        state["departments"].append(department)

        organisation = department["organisations"][0]
        description = item.get("description", "").strip()

        scheme = {
            "title": title,
            "introduced_on": item.get("introduced_on","").strip(),
            "valid_upto": None if item.get("valid_upto", "").strip() == "" else item["valid_upto"].strip(),
            "funding_pattern": item.get("funding_pattern", "").strip(),
            "description": description,
            "scheme_link": item.get("schemeUrl"),  
            "beneficiaries": [
                {"beneficiary_type": item.get("beneficiary", "").strip()}
            ],
            "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ], 
            "sponsors": [],  
            "criteria": item.get("criteria",""),
            "procedures": item.get("procedures",""),
            "benefits": [
                {"benefit_type": item.get("benefits", [])} 
            ],
            "tags": item.get("tags"),  # Implement determine_tags function
            "statistical_summary": []  # Exclude 'year' field from statistical summary
        }
        organisation["schemes"].append(scheme)

def transform_and_add_tripura_data(original_data, combined_data):
    state_name = "Tripura"

    for item in original_data:
        title = remove_leading_numbers(item.get("title", "").strip())


        state = {
            "state_name": state_name,
            "departments": []
        }
        combined_data["states"].append(state)

        department_name = item.get("department_name", "").strip()


        department = {
            "department_name": department_name,
            "organisations": [
                {
                    "organisation_name": department_name,
                    "schemes": []
                }
            ]
        }
        state["departments"].append(department)

        organisation = department["organisations"][0]
        description = item.get("description", "").strip()

        scheme = {
            "title": title,
            "introduced_on": item.get("introduced_on","").strip(),
            "valid_upto": None if item.get("valid_upto", "").strip() == "" else item["valid_upto"].strip(),
            "funding_pattern": item.get("funding_pattern", "").strip(),
            "description": description,
            "scheme_link": item.get("schemeUrl"),  
            "beneficiaries": [
                {"beneficiary_type": item.get("beneficiary", "").strip()}
            ],
            "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ], 
            "sponsors": [],  
            "criteria": item.get("criteria",""),
            "procedures": item.get("procedures",""),
            "benefits": [
                {"benefit_type": item.get("benefits", [])} 
            ],
            "tags": determine_tags(title, description),  # Implement determine_tags function
            "statistical_summary": []  # Exclude 'year' field from statistical summary
        }
        organisation["schemes"].append(scheme)



def transform_and_add_sikkim_data(original_data, combined_data):
    for item in original_data:
        state_name = "Sikkim"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)

def transform_and_add_telangana_data(original_data, combined_data):
    for item in original_data:
        state_name = "Telangana"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)
        
def transform_and_add_uttarakhand_data(original_data, combined_data):
    for item in original_data:
        state_name = "Uttarakhand"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)


def transform_and_add_delhi_data(original_data, combined_data):
    for item in original_data:
        state_name = "Delhi"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)

def transform_and_add_ladakh_data(original_data, combined_data):
    for item in original_data:
        state_name = "Ladakh"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)

# FROM HERE

def transform_and_add_punjab_data(original_data, combined_data):
    for item in original_data:
        state_name = "Punjab"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_andhra_pradesh_data(original_data, combined_data):
    for item in original_data:
        state_name = "Andhra Pradesh"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_haryana_data(original_data, combined_data):
    for item in original_data:
        state_name = "Haryana"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_assam_data(original_data, combined_data):
    for item in original_data:
        state_name = "Assam"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_odisha_data(original_data, combined_data):
    for item in original_data:
        state_name = "Odisha"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_chhattisgarh_data(original_data, combined_data):
    for item in original_data:
        state_name = "Chhattisgarh"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_chandigarh_data(original_data, combined_data):
    for item in original_data:
        state_name = "Chandigarh"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_arunchala_pradesh_data(original_data, combined_data):
    for item in original_data:
        state_name = "Arunchala Pradesh"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_dadra_and_nagar_haveli_data(original_data, combined_data):
    for item in original_data:
        state_name = "Dadra and Nagar Haveli"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)
def transform_and_add_nagaland_data(original_data, combined_data):
    for item in original_data:
        state_name = "Nagaland"
        created_at = "2024-06-25T12:00:00Z"
        department_name = item.get("department_name")
        state = next((s for s in combined_data["states"] if s["state_name"] == state_name), None)

        if not state:
            state = {
                "state_name": state_name,
                "created_at": created_at,
                "departments": []
            }
            combined_data["states"].append(state)

        department = next((d for d in state["departments"] if d["department_name"] == department_name), None)

        if not department:
            department = {
                "department_name": department_name,
                "created_at": created_at,
                "organisations": [
                    {
                        "organisation_name": department_name,
                        "created_at": created_at,
                        "schemes": []
                    }
                ]
            }
            state["departments"].append(department)

        organisation = department["organisations"][0]
        title = remove_leading_numbers(item.get("title").strip())
        description = item.get("description")
        scheme = {
            "title": title,
            "introduced_on": convert_date_format(item.get("introduced_on")),
            "valid_upto": item.get("valid_upto"),
            "funding_pattern": item.get("funding_pattern"),
            "description": description,
            "scheme_link": item.get("scheme_link"),
            "beneficiaries": [
                {"beneficiary_type": beneficiary_type} for beneficiary_type in item.get("beneficiaries", [])
            ] if item.get("beneficiaries") else [],
            "sponsors": [
                {"sponsor_type": sponsor_type} for sponsor_type in item.get("sponsors", [])
            ],
             "documents": [
                {"document_name": document} for document in item.get("documents", [])
            ],
            "criteria": [
                {"description": description} for description in item.get("criteria", [])
            ] if item.get("criteria") else [],
            "procedures": [
                {"step_description": step_description} for step_description in item.get("procedures", [])
            ],
            "tags": determine_tags(title, description) + item.get("tags", [])
        }
        organisation["schemes"].append(scheme)




# Read data from JSON files
with open(base_file_path+"/meghalaya.json", "r") as file:
    meghalaya_data = json.load(file)

with open(base_file_path+"/tamilnadu.json", "r") as file:
    tamilnadu_data = json.load(file)

with open(base_file_path+"/puducherry.json", "r") as file:
    puducherry_data = json.load(file)

with open(base_file_path+"/jammukashmir.json", "r") as file:
    jammukashmir_data = json.load(file)

with open(base_file_path+"/gujrat.json", "r") as file:
    gujarat_data = json.load(file)

with open(base_file_path+"/maharastra.json", "r") as file:
    maharashtra_data = json.load(file)

with open(base_file_path+"/up/up_youth_welfare.json", "r") as file:
    up_data = json.load(file)

with open(base_file_path+"/himachalPradesh.json", "r") as file:
    himachal_data = json.load(file)

with open(base_file_path+"/madhyaPradesh.json", "r") as file:
    madhyaPradesh_data = json.load(file)

with open(base_file_path+"/kerala.json", "r") as file:
    kerela_data = json.load(file)

with open(base_file_path+"/manipur.json", "r") as file:
    manipur_data = json.load(file)

with open(base_file_path+"/goa.json", "r") as file:
    goa_data = json.load(file)

with open(base_file_path+"/jharkhand.json", "r") as file:
    jharkhand_data = json.load(file)

with open(base_file_path+"/tripura.json", "r") as file:
    tripura_data = json.load(file)

with open(base_file_path+"/sikkim.json", "r") as file:
    sikkim_data = json.load(file)

with open(base_file_path+"/telangana.json", "r") as file:
    telangana_data = json.load(file)

with open(base_file_path+"/uttarakhand.json", "r") as file:
    uttarakhand_data = json.load(file)

with open(base_file_path+"/delhi.json", "r") as file:
    delhi_data = json.load(file)

with open(base_file_path+"/ladakh.json", "r") as file:
    ladakh_data = json.load(file)

# From this
with open(base_file_path+"/punjab.json", "r") as file:
    punjab_data = json.load(file)
with open(base_file_path+"/andhra.json", "r") as file:
    andhraPradesh_data = json.load(file)
with open(base_file_path+"/haryana.json", "r") as file:
    haryana_data = json.load(file)

with open(base_file_path+"/assam.json", "r") as file:
    assam_data = json.load(file)

with open(base_file_path+"/odisha.json", "r") as file:
    odisha_data = json.load(file)
with open(base_file_path+"/chhattisgarh.json", "r") as file:
    chhattisgarh_data = json.load(file)
with open(base_file_path+"/chandigarh.json", "r") as file:
    chandigarh_data = json.load(file)
with open(base_file_path+"/arunachalPradesh.json", "r") as file:
    arunachalPradesh_data = json.load(file)
with open(base_file_path+"/dadraAndNagarHaveli.json", "r") as file:
    dadraAndNagarHaveli_data = json.load(file)
# with open(base_file_path+"/nagaland.json", "r") as file:
#     nagaland_data = json.load(file)


# Initialize the combined data structure
combined_data = {
    "states": []
}

# Transform and add data to the combined structure
transform_and_add_meghalaya_data(meghalaya_data, combined_data)
transform_and_add_tamilnadu_data(tamilnadu_data, combined_data)
transform_and_add_puducherry_data(puducherry_data, combined_data)
transform_and_add_jammukashmir_data(jammukashmir_data, combined_data)
transform_and_add_gujarat_data(gujarat_data, combined_data)
transform_and_add_maharashtra_data(maharashtra_data, combined_data)
transform_and_add_uttar_pradesh_data(up_data,combined_data)
transform_and_add_himachal_pradesh_data(himachal_data,combined_data)
transform_and_add_madhya_pradesh_data(madhyaPradesh_data,combined_data)
transform_and_add_kerela_data(kerela_data,combined_data)
transform_and_add_manipur_data(manipur_data,combined_data)
transform_and_add_goa_data(goa_data,combined_data)
transform_and_add_jharkhand_data(jharkhand_data,combined_data)
transform_and_add_tripura_data(tripura_data,combined_data)
transform_and_add_sikkim_data(sikkim_data,combined_data)
transform_and_add_telangana_data(telangana_data,combined_data)
transform_and_add_uttarakhand_data(uttarakhand_data,combined_data)
transform_and_add_delhi_data(delhi_data,combined_data)
transform_and_add_ladakh_data(ladakh_data,combined_data)
# from here
transform_and_add_punjab_data(punjab_data,combined_data)# Pujab
transform_and_add_andhra_pradesh_data(andhraPradesh_data,combined_data)# AndhraPradesh
transform_and_add_haryana_data(haryana_data,combined_data)# Haryana
transform_and_add_assam_data(assam_data,combined_data)# Assam
transform_and_add_odisha_data(odisha_data,combined_data)# Odisha
transform_and_add_chhattisgarh_data(chhattisgarh_data,combined_data)# Chhattisgarh
transform_and_add_chandigarh_data(chandigarh_data,combined_data)# Chandigarh
transform_and_add_arunchala_pradesh_data(arunachalPradesh_data,combined_data)# Arunachal Pradesh
transform_and_add_dadra_and_nagar_haveli_data(dadraAndNagarHaveli_data,combined_data)# Dadra and Nagar haveli
# transform_and_add_nagaland_data(nagaland_data,combined_data)# Nagaland



# Save the combined data to a new JSON file
with open(base_file_path+"/combined_schemes_data.json", "w") as file:
    json.dump(combined_data, file,ensure_ascii=False, indent=4)

# print("Combined data has been successfully saved to combined_schemes_data.json")