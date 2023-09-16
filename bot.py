import os
import io
from pdf2image import convert_from_path
from pdfrw import PdfWriter, PdfReader
import ocr
# import utility
import json
from docx import Document
import shutil

current_path = os.getcwd()
print(current_path)

# Get the current value of the PATH environment variable
path_env_var = os.environ.get('PATH')
# print(f"path_env_var\n{path_env_var}")
# Append the current folder path to the PATH environment variable
updated_path_env_var = f"{current_path}\\poppler\\Library\\bin;{path_env_var}"
# print(f"updated_path_env_var\n{updated_path_env_var}")
# exit()
# Set the updated value back to the PATH environment variable
os.environ['PATH'] = updated_path_env_var
# files = [current_path + '\\Search Package\\' + f for f in os.listdir('./Search Package') if f.endswith('.pdf')]
files = [current_path + '\\' + f for f in os.listdir('./') if f.endswith('.pdf')]
# print()
# exit()

doc_index = 0

deed_array = ['Warranty Deed', 'Quit Claim Deed', 'QuitClaim Deed', 'Disclaimer Deed', 'Special Warranty Deed', 'Grant Deed', 'Trustees Deed upon Sale', "Trustee's Deed", 'Limited Warranty Deed', 'Bargain and sale deed', 'Administrator deeds', 'Sheriff Deed', 'Deed Under Power Of Sale', 'General Warranty Deed', 'North Carolina General Warranty Deed', 'This Deed', 'Deed', 'Release Deed']
deed_array = [deed.lower() for deed in deed_array]
mortgage_array = ['Deed of Trust', 'Security Deed', 'Mortgage', 'Partial Claims Mortgage', 'Short form Deed of Trust']
mortgage_array = [mortgage.lower() for mortgage in mortgage_array]
judgment_array = ['Abstract Judgment', 'Divorce Decree', 'Criminal Restitution Judgment', 'Notice of Lis Pendens', 'FIFA', 'Final Judgment']
judgment_array = [judgment.lower() for judgment in judgment_array]
liens_array = ['Water Lien', 'Sewer Lien', 'Federal Tax Lien', 'State Tax Lien', 'UCC Financing Statement', 'Homeowners Association Lien', 'Mechanic Lien', 'Notice and Claim of Lien', 'Tax Lien', 'Code Violation Lien', 'Notice of Pending Lien', 'Claim Of Lien', 'Notice Regarding Payment Of Support', 'Notice Of Federal Tax Lien', 'Statement Of Lien']
liens_array = [liens.lower() for liens in liens_array]
assignments_array = ['Assignment of Security Deed', 'Corporate Assignment of Deed of Trust', 'Assignment of Security Instrument', 'Assignment of First Mortgage and Assignment of Rents', 'Assignment of Mortgage']
assignments_array = [assignments.lower() for assignments in assignments_array]
modification_array = ['Loan Modification Agreement', 'Mortgage Modification Agreement', 'Agreement of Modification of Mortgage', 'Modification Agreement', 'FHA Home Affordable Modification Agreement']
modification_array = [modification.lower() for modification in modification_array]
substitution_array = ['Substitution Of Trustee', 'Appointment Of Substitute Trustees', 'Deed Of Appointment Of Substitute Trustee']
substitution_array = [substitution.lower() for substitution in substitution_array]


#List out all the directories using os.listdir()
dirs = os.listdir('./')

# #Iterate through each directory
# for dir in dirs:
#     #Join the path with the directory name
#     dir_path = os.path.join('./', dir)
    
#     #Check if it's a directory and not equals to 'Search'
#     if os.path.isdir(dir_path) and dir != 'Search Package':
#         #use shutil.rmtree() to remove the directory
#         shutil.rmtree(dir_path)

for file in files:
    filename = file.split("\\")[-1].split(".")[0]
    print('------------ ' + filename + ' -------------')
    reader = PdfReader(file)
    
    # print(file)
    images = convert_from_path(file)
    
    final_str = ""
    parcel_flag = 0
    count_judg = 1
    count_deed = 1
    count_assign = 1
    count_financial = 1
    deeds_str = ""
    additional_str = ""
    num_legal = 0
    prev_page_deed = 0
    deed_txt = ""
    financial_txt = ""
    prev_page_financial = 0

    # first_page = -1
    # last_page = -1
    doc_names = []
    pages = []

    for i, image in enumerate(images):
        # Save the image to a byte stream
        img_bytes = io.BytesIO()
        image.save(img_bytes, format='PNG')

        content = img_bytes.getvalue()
        # Run the OCR on the image
        result = ocr.textract_analysis(content)
        
        str_str = ""
        flag = 0
        reason = ""
        deed_flag = 0
        assign_flag = 0
        legal_flag = 0
        
        for sstr in result:
            str_str += sstr
            str_str += " "
        lower_str = str_str.lower()

        
        core_content = ""
        if len(lower_str) > 200:
            core_content = lower_str[0:200]
        else:
            core_content = lower_str
        print(lower_str)
        print('--------------------------------------------')
        if "Uniform Residential Loan Application".lower() in core_content:
            doc_names.append("Uniform Residential Loan Application")
            pages.append(i)
        if "Uniform Residential Appraisal Report".lower() in core_content:
            doc_names.append("Uniform Residential Appraisal Report")
            pages.append(i)
        if "Individual Income Tax Return".lower() in core_content:
            doc_names.append("Individual Income Tax Return")
            pages.append(i)
        if "Bank of America".lower() in core_content:
            doc_names.append("Bank of America")
            pages.append(i)
        if "Closing Disclosure".lower() in core_content:
            doc_names.append("Closing Disclosure")
            pages.append(i)
        if "Credit Report".lower() in core_content:
            doc_names.append("Credit Report")
            pages.append(i)
        if "Settlement Statement".lower() in core_content:
            doc_names.append("Settlement Statement")
            pages.append(i)
        if "PAY STUB".lower() in core_content:
            doc_names.append("PAY STUB")
            pages.append(i)
        if "Approval Letter".lower() in core_content:
            doc_names.append("Approval Letter")
            pages.append(i)
        if "22222".lower() in core_content:
            doc_names.append("22222")
            pages.append(i)


    print(doc_names)
    print(pages)
    for i in range(len(pages)):
        reader = PdfReader(file)
        pdf_writer = PdfWriter()

        # If it's the last index item, include all remaining pages
        if i == len(pages) - 1:
            for j in range(pages[i], len(reader.pages)):
                page = reader.pages[j]
                pdf_writer.addpage(page)
        else:
            for j in range(pages[i], pages[i+1]):
                page = reader.pages[j]
                pdf_writer.addpage(page)

        # Write the split PDF file
        with open(doc_names[i] + "_" + str(i+1) + ".pdf", "wb") as output_pdf:
            pdf_writer.write(output_pdf)

        # for doc_name in doc_names:
        #     if not os.path.exists('./' + doc_name):
        #         os.makedirs('./' + doc_name)
        #     names = [f.rsplit(' ', 1)[0] for f in os.listdir('./' + doc_name) if f.endswith('.pdf')]
        #     with open(f'./{doc_name}/{doc_names[i]} {names.count(doc_names[i]) + 1}.pdf', 'wb') as out:
        #         pdf_writer.write(out)


    # for index, page in enumerate(pages):
    #     try:
    #         page_tuple = (pages[index], pages[index+1])
    #     except:
    #         page_tuple = (pages[index], len(reader.pages) - 1)
    #     print(page_tuple)
    #     reader = PdfReader(file)
    #     writer = PdfWriter()
    #     page_range = range(page_tuple[0], page_tuple[1])
    #     print(page_range)

    #     for page_num, p in enumerate(reader.pages, 1):
    #         print('-----------')
    #         print(page_num, p)
    #         if page_num in page_range:
    #             print('============', page_num, p)
    #             writer.add_page(p)
    #     print(doc_names[index])
        


        # if doc_names[index].lower() in deed_array:
        #     if not os.path.exists('./' + filename + '/Deeds'):
        #         os.makedirs('./' + filename + '/Deeds')
        #     names = [f.rsplit(' ', 1)[0] for f in os.listdir('./' + filename + '/Deeds') if f.endswith('.pdf')]
        #     with open(f'./{filename}/Deeds/{doc_names[index]} {names.count(doc_names[index]) + 1}.pdf', 'wb') as out:
        #         writer.write(out)
        # elif doc_names[index].lower() in mortgage_array:
        #     if not os.path.exists('./' + filename + '/Mortgage'):
        #         os.makedirs('./' + filename + '/Mortgage')
        #     names = [f.rsplit(' ', 1)[0] for f in os.listdir('./' + filename + '/Mortgage') if f.endswith('.pdf')]
        #     with open(f'./{filename}/Mortgage/{doc_names[index]} {names.count(doc_names[index]) + 1}.pdf', 'wb') as out:
        #         writer.write(out)
        # elif doc_names[index].lower() in judgment_array:
        #     if not os.path.exists('./' + filename + '/Judgment'):
        #         os.makedirs('./' + filename + '/Judgment')
        #     names = [f.rsplit(' ', 1)[0] for f in os.listdir('./' + filename + '/Judgment') if f.endswith('.pdf')]
        #     with open(f'./{filename}/Judgment/{doc_names[index]} {names.count(doc_names[index]) + 1}.pdf', 'wb') as out:
        #         writer.write(out)
        # elif doc_names[index].lower() in liens_array:
        #     if not os.path.exists('./' + filename + '/Liens'):
        #         os.makedirs('./' + filename + '/Liens')
        #     names = [f.rsplit(' ', 1)[0] for f in os.listdir('./' + filename + '/Liens') if f.endswith('.pdf')]
        #     with open(f'./{filename}/Liens/{doc_names[index]} {names.count(doc_names[index]) + 1}.pdf', 'wb') as out:
        #         writer.write(out)
        # elif doc_names[index].lower() in assignments_array:
        #     if not os.path.exists('./' + filename + '/Assignments'):
        #         os.makedirs('./' + filename + '/Assignments')
        #     names = [f.rsplit(' ', 1)[0] for f in os.listdir('./' + filename + '/Assignments') if f.endswith('.pdf')]
        #     with open(f'./{filename}/Assignments/{doc_names[index]} {names.count(doc_names[index]) + 1}.pdf', 'wb') as out:
        #         writer.write(out)
        # elif doc_names[index].lower() in modification_array:
        #     if not os.path.exists('./' + filename + '/Modification'):
        #         os.makedirs('./' + filename + '/Modification')
        #     names = [f.rsplit(' ', 1)[0] for f in os.listdir('./' + filename + '/Modification') if f.endswith('.pdf')]
        #     with open(f'./{filename}/Modification/{doc_names[index]} {names.count(doc_names[index]) + 1}.pdf', 'wb') as out:
        #         writer.write(out)
        # elif doc_names[index].lower() in substitution_array:
        #     if not os.path.exists('./' + filename + '/Substitution'):
        #         os.makedirs('./' + filename + '/Substitution')
        #     names = [f.rsplit(' ', 1)[0] for f in os.listdir('./' + filename + '/Substitution') if f.endswith('.pdf')]
        #     with open(f'./{filename}/Substitution/{doc_names[index]} {names.count(doc_names[index]) + 1}.pdf', 'wb') as out:
        #         writer.write(out)


