# import json
# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from myapp.models import State, Department, Organisation, Scheme, Beneficiary, Document, Sponsor, SchemeBeneficiary, SchemeDocument, SchemeSponsor, Criteria, Procedure
# import google.generativeai as genai
# import google.generativeai.protos as protos
# import textwrap 
# import os 

# api_key = os.getenv('GOOGLE_API_KEY')
# genai.configure(api_key=api_key)

# scheme_schema = genai.protos.Schema(
#     type=genai.protos.Type.OBJECT,
#     properties={
#         'title': genai.protos.Schema(type=genai.protos.Type.STRING),
#         'introduced_on': genai.protos.Schema(type=genai.protos.Type.STRING),
#         'valid_upto': genai.protos.Schema(type=genai.protos.Type.STRING),
#         'funding_pattern': genai.protos.Schema(type=genai.protos.Type.STRING),
#         'description': genai.protos.Schema(type=genai.protos.Type.STRING),
#         'scheme_link': genai.protos.Schema(type=genai.protos.Type.STRING),
#         'beneficiaries': genai.protos.Schema(type=genai.protos.Type.ARRAY, items=genai.protos.Schema(type=genai.protos.Type.OBJECT, properties={
#             'beneficiary_type': genai.protos.Schema(type=genai.protos.Type.STRING)
#         })),
#         'documents': genai.protos.Schema(type=genai.protos.Type.ARRAY, items=genai.protos.Schema(type=genai.protos.Type.OBJECT, properties={
#             'document_name': genai.protos.Schema(type=genai.protos.Type.STRING)
#         })),
#         'sponsors': genai.protos.Schema(type=genai.protos.Type.ARRAY, items=genai.protos.Schema(type=genai.protos.Type.OBJECT, properties={
#             'sponsor_type': genai.protos.Schema(type=genai.protos.Type.STRING)
#         })),
#         'criteria': genai.protos.Schema(type=genai.protos.Type.ARRAY, items=genai.protos.Schema(type=genai.protos.Type.OBJECT, properties={
#             'description': genai.protos.Schema(type=genai.protos.Type.STRING),
#             'value': genai.protos.Schema(type=genai.protos.Type.STRING)
#         })),
#         'procedures': genai.protos.Schema(type=genai.protos.Type.ARRAY, items=genai.protos.Schema(type=genai.protos.Type.OBJECT, properties={
#             'step_description': genai.protos.Schema(type=genai.protos.Type.STRING)
#         }))
#     },
#     required=['title', 'description', 'scheme_link']
# )

# main_schema = genai.protos.Schema(
#     type=genai.protos.Type.OBJECT,
#     properties={
#         'states': genai.protos.Schema(type=genai.protos.Type.ARRAY, items=genai.protos.Schema(type=genai.protos.Type.OBJECT, properties={
#             'state_name': genai.protos.Schema(type=genai.protos.Type.STRING),
#             'departments': genai.protos.Schema(type=genai.protos.Type.ARRAY, items=genai.protos.Schema(type=genai.protos.Type.OBJECT, properties={
#                 'department_name': genai.protos.Schema(type=genai.protos.Type.STRING),
#                 'organisations': genai.protos.Schema(type=genai.protos.Type.ARRAY, items=genai.protos.Schema(type=genai.protos.Type.OBJECT, properties={
#                     'organisation_name': genai.protos.Schema(type=genai.protos.Type.STRING),
#                     'schemes': genai.protos.Schema(type=genai.protos.Type.ARRAY, items=scheme_schema)
#                 }))
#             }))
#         }))
#     },
#     required=['states']
# )
# add_to_database = genai.protos.FunctionDeclaration(
#     name="add_to_database",
#     description=textwrap.dedent("""\
#         Adds entities to the database.
#         """),
#     parameters=main_schema
# )

# def validate_and_structure_data(data, schema):
#     # Initialize the Gemini model with the function declaration
#     model = genai.GenerativeModel(
#         model_name='models/gemini-1.5-pro-latest',
#         tools=[add_to_database]
#     )

#     # Generate content using the Gemini API
#     result = model.generate_content(
#         f"Please validate and structure the following data according to the provided schema:\n\n{json.dumps(data, indent=4)}",
#         tool_config={'function_calling_config': 'ANY'}
#     )

#     structured_data = {}
    
#     # Iterate over parts of the Gemini API response
#     for part in result.candidates[0].content.parts:
#         if part.function_call:
#             # Convert the function call result to a JSON compatible object
#             part_data = json.loads(json.dumps(type(part.function_call).to_dict(part.function_call)))
#             structured_data.update(part_data)

#     return structured_data

    

# class Command(BaseCommand):
#     help = 'Load data from JSON file into database'
#     def handle(self, *args, **kwargs):
#         with open('/Users/salonisharma/backend-roorkee-final/backend-roorkee/myapp/jammukashmir.json', 'r') as file:
#             data = json.load(file)
#             # self.stdout.write(f'Read JSON data: {json.dumps(data, indent=4)}')  # Logging for verification

#             structured_data = validate_and_structure_data(data, main_schema)
            
#             # Print the structured data returned by Gemini
#             self.stdout.write(self.style.SUCCESS('Structured Data Generated by Gemini:'))
#             self.stdout.write(json.dumps(structured_data, indent=4))

import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from myapp.models import State, Department, Organisation, Scheme, Beneficiary, Document, Sponsor, SchemeBeneficiary, SchemeDocument, SchemeSponsor, Criteria, Procedure
import google.generativeai as genai
import google.generativeai.protos as protos
import textwrap 
import os 

# Configure the Google API key
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

# Define Beneficiary schema
# beneficiary_schema = genai.protos.Schema(
#     type=genai.protos.Type.OBJECT,
#     properties={
#         'beneficiary_type': genai.protos.Schema(type=genai.protos.Type.STRING)
#     },
#     required=['beneficiary_type']
# )

# # Define Document schema
# document_schema = genai.protos.Schema(
#     type=genai.protos.Type.OBJECT,
#     properties={
#         'document_name': genai.protos.Schema(type=genai.protos.Type.STRING)
#     },
#     required=['document_name']
# )

# # Define Sponsor schema
# sponsor_schema = genai.protos.Schema(
#     type=genai.protos.Type.OBJECT,
#     properties={
#         'sponsor_type': genai.protos.Schema(type=genai.protos.Type.STRING)
#     },
#     required=['sponsor_type']
# )

# # Define Criteria schema
# criteria_schema = genai.protos.Schema(
#     type=genai.protos.Type.OBJECT,
#     properties={
#         'description': genai.protos.Schema(type=genai.protos.Type.STRING),
#         'value': genai.protos.Schema(type=genai.protos.Type.STRING)
#     },
#     required=['description', 'value']
# )

# # Define Procedure schema
# procedure_schema = genai.protos.Schema(
#     type=genai.protos.Type.OBJECT,
#     properties={
#         'step_description': genai.protos.Schema(type=genai.protos.Type.STRING)
#     },
#     required=['step_description']
# )

# # Define Scheme schema
# scheme_schema = genai.protos.Schema(
#     type=genai.protos.Type.OBJECT,
#     properties={
#         'title': genai.protos.Schema(type=genai.protos.Type.STRING),
#         'introduced_on': genai.protos.Schema(type=genai.protos.Type.STRING),
#         'valid_upto': genai.protos.Schema(type=genai.protos.Type.STRING),
#         'funding_pattern': genai.protos.Schema(type=genai.protos.Type.STRING),
#         'description': genai.protos.Schema(type=genai.protos.Type.STRING),
#         'scheme_link': genai.protos.Schema(type=genai.protos.Type.STRING),
#         'beneficiaries': genai.protos.Schema(
#             type=genai.protos.Type.ARRAY,
#             items=beneficiary_schema
#         ),
#         'documents': genai.protos.Schema(
#             type=genai.protos.Type.ARRAY,
#             items=document_schema
#         ),
#         'sponsors': genai.protos.Schema(
#             type=genai.protos.Type.ARRAY,
#             items=sponsor_schema
#         ),
#         'criteria': genai.protos.Schema(
#             type=genai.protos.Type.ARRAY,
#             items=criteria_schema
#         ),
#         'procedures': genai.protos.Schema(
#             type=genai.protos.Type.ARRAY,
#             items=procedure_schema
#         )
#     },
#     required=['title', 'description', 'scheme_link']
# )

# # Define Organisation schema
# organisation_schema = genai.protos.Schema(
#     type=genai.protos.Type.OBJECT,
#     properties={
#         'organisation_name': genai.protos.Schema(type=genai.protos.Type.STRING),
#         'schemes': genai.protos.Schema(
#             type=genai.protos.Type.ARRAY,
#             items=scheme_schema
#         )
#     },
#     required=['organisation_name']
# )

# # Define Department schema
# department_schema = genai.protos.Schema(
#     type=genai.protos.Type.OBJECT,
#     properties={
#         'department_name': genai.protos.Schema(type=genai.protos.Type.STRING),
#         'organisations': genai.protos.Schema(
#             type=genai.protos.Type.ARRAY,
#             items=organisation_schema
#         )
#     },
#     required=['department_name']
# )

# # Define State schema
# state_schema = genai.protos.Schema(
#     type=genai.protos.Type.OBJECT,
#     properties={
#         'state_name': genai.protos.Schema(type=genai.protos.Type.STRING),
#         'departments': genai.protos.Schema(
#             type=genai.protos.Type.ARRAY,
#             items=department_schema
#         )
#     },
#     required=['state_name']
# )

# # Define Main schema
# main_schema = genai.protos.Schema(
#     type=genai.protos.Type.OBJECT,
#     properties={
#         'states': genai.protos.Schema(
#             type=genai.protos.Type.ARRAY,
#             items=state_schema
#         )
#     },
#     required=['states']
# )
description_schema = genai.protos.Schema(
    type=genai.protos.Type.OBJECT,
    properties={
        'sponsorship_type': genai.protos.Schema(type=genai.protos.Type.STRING),
        'beneficiaries': genai.protos.Schema(
            type=genai.protos.Type.ARRAY,
            items=genai.protos.Schema(type=genai.protos.Type.STRING)
        ),
        'benefit_type': genai.protos.Schema(type=genai.protos.Type.STRING),
        'eligibility': genai.protos.Schema(type=genai.protos.Type.STRING)
    },
    required=['sponsorship_type', 'beneficiaries', 'benefit_type', 'eligibility']
)
procedure_schema = genai.protos.Schema(
    type=genai.protos.Type.OBJECT,
    properties={
        'Procedure': genai.protos.Schema(
            type=genai.protos.Type.OBJECT,
            properties={
                'Availability': genai.protos.Schema(type=genai.protos.Type.STRING),
                'Completion': genai.protos.Schema(type=genai.protos.Type.STRING),
                'Submission': genai.protos.Schema(type=genai.protos.Type.STRING),
                'Consolidation': genai.protos.Schema(type=genai.protos.Type.STRING),
                'Sanctioning Process': genai.protos.Schema(type=genai.protos.Type.STRING)
            },
            required=['Availability', 'Completion', 'Submission', 'Consolidation', 'Sanctioning Process']
        )
    },
    required=['Procedure']
)

# Define the function declaration for adding to the database
# add_to_database = genai.protos.FunctionDeclaration(
#     name="add_to_database",
#     description=textwrap.dedent("""\
#         Adds entities to the database.
#         """),
#     parameters=main_schema
# )
add_to_database = genai.protos.FunctionDeclaration(
    name="add_to_database",
    description=textwrap.dedent("""\
        Adds entities to the database.
        """),
    parameters=genai.protos.Schema(
        type=genai.protos.Type.OBJECT,
        properties={
            'description': description_schema,
            'procedure': procedure_schema
        },
        required=['description', 'procedure']
    )
)


# Function to validate and structure data using the Gemini API
def validate_and_structure_data(data, schema):
    # Initialize the Gemini model with the function declaration
    model = genai.GenerativeModel(
        model_name='models/gemini-1.5-pro-latest',
        tools=[add_to_database]
    )

    # Generate content using the Gemini API
    result = model.generate_content(
        f"Please validate and structure the following data according to the provided schema:\n\n{json.dumps(data, indent=4)}",
        tool_config={'function_calling_config': 'ANY'}
    )

    structured_data = {}
    
    # Iterate over parts of the Gemini API response
    for part in result.candidates[0].content.parts:
        if part.function_call:
            # Convert the function call result to a JSON compatible object
            part_data = json.loads(json.dumps(type(part.function_call).to_dict(part.function_call)))
            structured_data.update(part_data)

    return structured_data

# Django management command

class Command(BaseCommand):
    help = 'Load data from JSON file into database'

    def handle(self, *args, **kwargs):
        with open('/Users/salonisharma/backend-roorkee-final/backend-roorkee/myapp/jammukashmir.json', 'r') as file:
            data = json.load(file)
            
            # Extract description and procedure fields from your data
            structured_data = []
            for item in data:
                schemes = item.get('schemes', [])
                for scheme in schemes:
                    description = scheme.get('details', {}).get('Description of the Scheme', {})
                    procedure = scheme.get('details', {}).get('Procedure', {})
                    
                    # Validate and structure description and procedure using Gemini API
                    structured_description = validate_and_structure_data(description, description_schema)
                    structured_procedure = validate_and_structure_data(procedure, procedure_schema)
                    
                    # Append structured data to result list
                    structured_data.append({
                        'description': structured_description,
                        'procedure': structured_procedure
                    })

            # Print the structured data returned by Gemini for description and procedure
            self.stdout.write(self.style.SUCCESS('Structured Data Generated by Gemini:'))
            self.stdout.write(json.dumps(structured_data, indent=4))
# # class Command(BaseCommand):
#     help = 'Load data from JSON file into database'

#     def handle(self, *args, **kwargs):
#         with open('/Users/salonisharma/backend-roorkee-final/backend-roorkee/myapp/jammukashmir.json', 'r') as file:
#             data = json.load(file)
#             # self.stdout.write(f'Read JSON data: {json.dumps(data, indent=4)}')  # Logging for verification

#             structured_data = validate_and_structure_data(data, main_schema)
            
#             # Print the structured data returned by Gemini
#             self.stdout.write(self.style.SUCCESS('Structured Data Generated by Gemini:'))
#             self.stdout.write(json.dumps(structured_data, indent=4))



    # def handle(self, *args, **kwargs):
    #     with open('myapp/schemes.json', 'r') as file:
    #         data = json.load(file)
    #         structured_data = validate_and_structure_data(data, main_schema)
            
    #         # Load the structured data into the database
    #         self.load_data(structured_data)
        
    #         # self.load_data(data)
        
    #     self.stdout.write(self.style.SUCCESS('Successfully loaded data into database'))

    # def load_data(self, structured_data):
    #     for state_data in  structured_data['states']:
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  
    #         state, created = State.objects.get_or_create(
    #             state_name=state_data['state_name']
    #         )  

    #         for department_data in state_data['departments']:
    #             department, created = Department.objects.get_or_create(
    #                 state=state,
    #                 department_name=department_data['department_name']
    #             )

    #             for organisation_data in department_data['organisations']:
    #                 organisation, created = Organisation.objects.get_or_create(
    #                     department=department,
    #                     organisation_name=organisation_data['organisation_name']
    #                 )

    #                 for scheme_data in organisation_data['schemes']:
    #                     scheme, created = Scheme.objects.get_or_create(
    #                         title=scheme_data['title'],
    #                         department=department,
    #                         defaults={
    #                             'introduced_on': scheme_data.get('introduced_on'),
    #                             'valid_upto': scheme_data.get('valid_upto'),
    #                             'funding_pattern': scheme_data.get('funding_pattern', 'State'),
    #                             'description': scheme_data.get('description'),
    #                             'scheme_link': scheme_data.get('scheme_link')
    #                         }
    #                     )
    #                     if not created:
    #                         scheme.introduced_on = scheme_data.get('introduced_on')
    #                         scheme.valid_upto = scheme_data.get('valid_upto')
    #                         scheme.funding_pattern = scheme_data.get('funding_pattern', 'State')
    #                         scheme.description = scheme_data.get('description')
    #                         scheme.scheme_link = scheme_data.get('scheme_link')
    #                         scheme.save()

    #                     for beneficiary_data in scheme_data['beneficiaries']:
    #                         beneficiary, created = Beneficiary.objects.get_or_create(
    #                             beneficiary_type=beneficiary_data['beneficiary_type']
    #                         )
    #                         SchemeBeneficiary.objects.get_or_create(
    #                             scheme=scheme,
    #                             beneficiary=beneficiary
    #                         )

    #                     for document_data in scheme_data['documents']:
    #                         document, created = Document.objects.get_or_create(
    #                             document_name=document_data['document_name']
    #                         )
    #                         SchemeDocument.objects.get_or_create(
    #                             scheme=scheme,
    #                             document=document
    #                         )

    #                     for sponsor_data in scheme_data['sponsors']:
    #                         sponsor, created = Sponsor.objects.get_or_create(
    #                             sponsor_type=sponsor_data['sponsor_type']
    #                         )
    #                         SchemeSponsor.objects.get_or_create(
    #                             scheme=scheme,
    #                             sponsor=sponsor
    #                         )

    #                     for criteria_data in scheme_data['criteria']:
    #                         Criteria.objects.update_or_create(
    #                             scheme=scheme,
    #                             description=criteria_data['description'],
    #                             defaults={
    #                                 'value': criteria_data.get('value')
    #                             }
    #                         )

    #                     for procedure_data in scheme_data['procedures']:
    #                         Procedure.objects.update_or_create(
    #                             scheme=scheme,
    #                             step_description=procedure_data['step_description']
    #                         )

