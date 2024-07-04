import datetime
from django import template

register = template.Library()





@register.simple_tag
def Current_quarter():
    date = datetime.datetime.today()
    now = date.month
    year = date.year
    # + relativedelta(months=+5)

    if now in [5,6,7]:
        quarter="Q1'"+ str(year + 1)[-2:]
        return quarter
    elif now in [8,9,10] :
        quarter="Q2'"+ str(year + 1)[-2:]
        return quarter
    elif now in [11,12,1] :
        if now == 1:
            quarter="Q3'"+ str(year)[-2:]
        else:
            quarter="Q3'"+ str(year + 1)[-2:]
        return quarter
    elif now in [2,3,4] :
        quarter="Q4'"+ str(year)[-2:]
        return quarter
    else:
        raise ValueError('The Month is Incorrect')  
    
    
    
    
    
    
    
    
    
    

@register.simple_tag
def get_Next_quarter(q=4,s=Current_quarter(),this_quarter=False,prefix='',suffix=''):
    # print('into next quarter')
    year=int(s[3:])
    Q=int(s[1:2])
    quarter=[]
    for x in range(q):
        Q=1 if Q>3 else Q+1
        year=year+1 if Q==1 else year
        quarter.append(f'''Q{Q}'{year}''')
    if this_quarter:
        quarter.insert(0,f'''{prefix}{s}{suffix}''')
        print('nex',quarter)

    return quarter

@register.simple_tag
def get_previous_quarter(q=4,s=Current_quarter(),this_quarter=False,prefix='',suffix=''):
    year=int(s[3:])
    Q=int(s[1:2])
    # print('Current Quarter',s)
    quarter=[]
    for x in range(q):
        Q=4 if Q<2 else Q-1
        year=year-1 if Q==4 else year
        quarter.append(f'''{prefix}Q{Q}'{year}{suffix}''')
    if this_quarter:
        quarter.insert(0,f'''{prefix}{s}{suffix}''')
        print('pre',quarter)
    return quarter