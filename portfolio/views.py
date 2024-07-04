from io import BytesIO
import mimetypes
import os
import re
from wsgiref.types import FileWrapper
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
import pandas as pd
from django.utils.encoding import smart_str
from portfolio.templatetags.quality_tags import *

from iness import settings
from .models import *

from django.core.files.storage import FileSystemStorage

# Create your views here.


def home(request):
    quarter=Current_quarter()
    return redirect(reverse('dashboard', kwargs={'quarter': quarter}))



def dashboard(request,quarter):
    data = reval_file.objects.filter(quarter=quarter).values()
    print(quarter,"]][]][  ]")
    # return JsonResponse({"data":list(data)},safe=False)
    return render(request, "main.html", {"quarter":quarter,"data": data})


def signin(request):
    return render(request, "tables/test.html")


def file_upload(request):
    # print("++++++++++++++++++++++++++++=")
    try:
        if request.method == "POST":
            file = request.FILES["file"]
            quarter = request.POST.get("quarter")
            data = pd.read_excel(file, engine="openpyxl")

            data.fillna("0", inplace=True)
            # data.dropna(subset=['Site', 'PN'],how='any',inplace=True)
        
            # data=data.replace({np.NaN: None})
            # delete= icc_quanta.objects.filter(quarter = quarter).delete()
            row_iter = data.iterrows()
            # print("111")
            bulk_update = []
            for index, row in row_iter:
           
                revel_data = reval_file(
                    quarter=quarter,
                    item=row["Item"],
                    pn=row["PN"],
                    description=row["Description"],
                    qty=row["Qty"],
                    usd=row["Rework fee(USD)"],
                    scrap=row["Scrap Material"],
                    unit_freight=row["Unit Freight (USD)"],
                    unit_price=row["Unit  price (USD)"],
                    ext_price=row["Ext price (USD)"],
                    remark=row["Remark"],
                )
                revel_data.save()
            return redirect("/")
    except:
        pass


def reval_data(request):
    quarter=request.POST.get('quarter')
    if quarter== None:
        quarter='Q1'
    else:
        quarter=quarter

   
    data = reval_file.objects.filter(quarter=quarter).values()
    print(quarter,"]][]][  ]")
    return JsonResponse({"data":list(data)},safe=False)


# from openpyxl.worksheet.datavalidation import data


def download_Iness_bulkapproval(request, quarter):
    columns = [
        "item",
        "quarter",
        "pn",
        "description",
        "qty",
        "usd",
        "scrap",
        "unit_freight",
        "unit_price",
        "ext_price",
        "remark",
        "status",
        "approval_comments",
    ]
    alias = [
        "item",
        "quarter",
        "pn",
        "description",
        "qty",
        "usd",
        "scrap",
        "unit_freight",
        "unit_price",
        "ext_price",
        "remark",
        "status",
        "approval_comments",
    ]

    with BytesIO() as b:
        with pd.ExcelWriter(b, engine="xlsxwriter") as writer:
            data = reval_file.objects.filter(quarter=quarter).values_list(*columns)
            df = pd.DataFrame(data, columns=columns)

            df.to_excel(writer, index=False, header=alias, sheet_name="Sheet1")

            workbook = writer.book
            worksheet = writer.sheets["Sheet1"]

            money_format = workbook.add_format({"num_format": "$#,##0.0000"})

            header_format_3 = workbook.add_format(
                {
                    "bold": True,
                    "text_wrap": True,
                    "valign": "top",
                    "fg_color": "green",
                    "color": "white",
                    "border": 1,
                }
            )

            # Apply the header format
            for col_num in range(len(alias)):
                if alias[col_num] in ["status", "approval_comments"]:
                    worksheet.write(0, col_num, alias[col_num], header_format_3)
                else:
                    worksheet.write(0, col_num, alias[col_num])

            # Apply data validation for the "status" column
            worksheet.data_validation(
                "L2:L1048576", {"validate": "list", "source": ["Approved", "Rejected"]}
            )

        response = HttpResponse(b.getvalue(), content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = (
            'inline; filename="QP InESS Bulk upload All Parts.xlsx"'
        )
        return response



def download_template(request):
    download_file = os.path.join(settings.RESOURCES_ROOT, 'Rework Input template.xlsx')

    file_mimetype, _ = mimetypes.guess_type(download_file)
    print("download file", file_mimetype)

    response = FileResponse(open(download_file, 'rb'), content_type=file_mimetype)
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('Rework Input template.xlsx')
    response['Content-Length'] = os.path.getsize(download_file)

    return response




# def download_icc_quanta_waterfall_template(request):
#     download_file = settings.RESOURCES_ROOT+'/'+'Rework Input template.xlsx'
#     file_mimetype = mimetypes.guess_type(download_file)
#     file_wrapper = FileWrapper(open(download_file, 'rb'))
#     response = HttpResponse(file_wrapper, content_type=file_mimetype)
#     response['X-Sendfile'] = download_file
#     response['Content-Length'] = os.stat(download_file).st_size
#     response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('Rework Input template.xlsx')
#     return response


def QP_iness_bulk_upload(request):

    quarter = request.POST.get("quarter")
    print(quarter)
    file = request.FILES["QP_upload_file"]
    qp_data = reval_file.objects.filter(quarter=quarter)
    # df = pd.read_excel(excel)

    data = pd.read_excel(file)
    data.fillna("", inplace=True)

    for qp in qp_data:

        # df = data.replace({0: None, 'nan': ''})
        partnumber = data[(data["pn"] == qp.pn) & (data["quarter"] == qp.quarter)]

        approval_status = ""
        comments = ""

        if not partnumber.empty:
            iness_approval_status = partnumber["status"].values[0]
            iness_comments = partnumber["approval_comments"].values[0]

            # Convert NaN values to empty strings
            approval_status = (
                "" if pd.isna(iness_approval_status) else str(iness_approval_status)
            )
            comments = "" if pd.isna(iness_comments) else str(iness_comments)

        # Update the database with the retrieved values
        data_quanta = reval_file.objects.filter(id=qp.id, quarter=quarter).update(
            status=approval_status, approval_comments=comments
        )

    return redirect("/")

def qp_bulk_attchments(request):
    try:
        if request.method == "POST":
            files = request.FILES.getlist('bulk_files')
            quarter = request.POST.get("quarter")
            for i in files:
               
                fs = FileSystemStorage()
                name =  "_" + \
                randomString(10) + "." + \
                    re.sub('[^A-Za-z0-9\n\.]+', '', i.name)
                filename = fs.save('Files/'+name, i)
                # print(i.name.split('.')[0],"nmmm")
                ssr=i.name.split('.')[0]
 
                bulk_files = bulk_attchements(
                   
                    file=ssr, 
                    quarter=quarter,
                    stored_name=name
                )
                bulk_files.save()
       

        return redirect("/")
    except Exception as e:
     
        return HttpResponse("Error occurred while processing the request.")


import random
import string

def randomString(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters_and_digits) for i in range(length))
    return result_str





def bulk_files(request):
    try:
        data=bulk_attchements.objects.all().values()
  
        return JsonResponse({"data":list(data)},safe=True)
    except Exception as e:
        pass
    
    
    
def downloadmdfile(request, id):
    file = bulk_attchements.objects.filter(id=id).first()
    
    fs = FileSystemStorage()
    if fs.exists('Files/'+file.stored_name):
        fh = fs.open('Files/'+file.stored_name)
        response = HttpResponse(
        fh.read(), content_type="application/image/text")
        response['Content-Disposition'] = 'inline; filename=' + file.stored_name
        return response