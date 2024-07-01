from io import BytesIO
import mimetypes
from wsgiref.types import FileWrapper
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
import pandas as pd
from django.utils.encoding import smart_str

from iness import settings
from .models import *

# Create your views here.


def home(request):
    data = reval_file.objects.all()
    print(data,"ppp")
    return render(request, "main.html", {"data": data})


def signin(request):
    return render(request, "tables/test.html")


def file_upload(request):
    print("++++++++++++++++++++++++++++=")
    try:
        if request.method == "POST":
            file = request.FILES["file"]
            quarter = request.POST.get('quarter')
            data = pd.read_excel(file, engine="openpyxl")
            
            data.fillna("0", inplace=True)
            # data.dropna(subset=['Site', 'PN'],how='any',inplace=True)
            print(quarter,"[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]")
            # data=data.replace({np.NaN: None})
            # delete= icc_quanta.objects.filter(quarter = quarter).delete()
            row_iter = data.iterrows()
            # print("111")
            bulk_update = []
            for index, row in row_iter:
                print(row["Item"])
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
    data = reval_file.objects.all()
    print(data,"ppp")
    return render(request, "main.html", {"data": data})





# from openpyxl.worksheet.datavalidation import data

def download_Iness_bulkapproval(request, quarter="Q1"):
    columns = ['item', 'quarter', 'pn', 'description', 'qty', 'usd', 'scrap', 'unit_freight', 'unit_price', 'ext_price', 'remark','status','approval_comments']
    alias = ['item', 'quarter', 'pn', 'description','qty', 'usd', 'scrap', 'unit_freight'   , 'unit_price', 'ext_price', ' remark', 'status','approval_comments']
    
    with BytesIO() as b:
        with pd.ExcelWriter(b) as writer:
            data = reval_file.objects.filter(quarter=quarter).values_list(*columns)
            df = pd.DataFrame(data, columns=columns)

            df.to_excel(writer, index=False, header=alias, sheet_name="Sheet1")

            worksheet = writer.sheets['Sheet1']
            workbook = writer.book
            money = workbook.add_format({'num_format': '$#,##0.0000'})
            
            header_format_3 = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': 'green',
            'color':'white',
            'border': 1})
            # Add data validation for the "status" column
            
            worksheet.set_column('L:M',None,header_format_3)
            worksheet.data_validation('S1:S1048576', {'validate': 'list', 'source': ['Approved', 'Rejected']})
            writer.close()
            dv = workbook.data_validation
            dv.add(worksheet['S1:S1048576'], {'validate': 'list', 'source': ['Approved', 'Rejected']})

        response = HttpResponse(b.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'inline; filename="ICC Quanta InESS Bulk upload All Parts.xlsx"'
        return response
    
    
    
    
    
    
    
    
    
    
    
   
    
    
    # columns = ['item', 'quarter', 'pn', 'description', 'qty', 'usd', 'scrap', 'unit_freight', 'unit_price','ext_price','remark','status','approval_comments']
    

    # alias = ['item', 'quarter', 'pn', 'description','qty', 'usd', 'scrap', 'unit_freight'   , 'unit_price', 'ext_price', ' remark', 'status','approval_comments']
    # type='All'
    # with BytesIO() as b:
    #   with pd.ExcelWriter(b) as writer:
    #         df1 = pd.DataFrame(reval_file.objects.filter(quarter=quarter).values_list(*columns), columns=columns)
        
    #         df1.to_excel(writer, index=False, header=alias, sheet_name="Sheet1")
    #         sheet_names = writer.sheets.get_sheet_names()
    #         if sheet_names:
    #             worksheet = writer.sheets[sheet_names[0]]  # Access the first sheet
    #             # Rest of your code
    #         else:
    #             print("No sheets found")
    #         # workbook = writer.book
    #         # money = workbook.add_format({'num_format': '$#,##0.0000'})

    #         # # header_format_3 = workbook.add_format({
    #         # 'bold': True,
    #         # 'text_wrap': True,
    #         # 'valign': 'top',
    #         # 'fg_color': 'green',
    #         # 'color':'white',
    #         # 'border': 1})

    #         # worksheet.set_column('S:T',None,header_format_3)
    #         # worksheet.data_validation('S1:S1048576', {'validate': 'list', 'source': ['Approved', 'Rejected']})
    #         # writer.save()

    #         response = HttpResponse(b.getvalue(), content_type='application/vnd.ms-excel')
    #         response['Content-Disposition'] = f'inline; filename="ICC Quanta InESS Bulk upload ' + type + ' Parts.xlsx"'
    #         return response





# def download_icc_quanta_template(request):
#     download_file = settings.RESOURCES_ROOT+'/'+'Quanta ICC Template.xlsx'
#     file_mimetype = mimetypes.guess_type(download_file)
#     file_wrapper = FileWrapper(open(download_file, 'rb'))
#     response = HttpResponse(file_wrapper, content_type=file_mimetype)
#     response['X-Sendfile'] = download_file
#     response['Content-Length'] = os.stat(download_file).st_size
#     response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('Quanta ICC Template.xlsx')
#     return response 