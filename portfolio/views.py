from django.http import JsonResponse
from django.shortcuts import redirect, render
import pandas as pd
from .models import *

# Create your views here.


def home(request):
    return render(request, "main.html")


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





def item_list(request):
    items = reval_file.objects.all()
    data = [{"name": item.quarter, "description": item.item, "price": str(item.unit_freight)} for item in items]
    return JsonResponse(data, safe=False)