from ast import If
from email.mime import image
from email.policy import default
from genericpath import exists
from heapq import merge
from http.client import HTTPResponse
from optparse import Values
from time import sleep
from urllib.error import HTTPError
from urllib.parse import urlparse
# Create your views here.
from django.shortcuts import render
from shopify_auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse ,JsonResponse
import json
import requests
import shopify 
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.utils import timezone
from .models import AuthAppShopUser
from .models import Billing
from requests.exceptions import ConnectionError
import os
import validators
import traceback


@login_required
def check_user_billing(request):
    if request.user.is_authenticated:
        with request.user.session:
            userbilling=Billing.objects.filter(user=request.user.id).order_by('-id').first()
            if userbilling:
                try:
                    user_charge=shopify.RecurringApplicationCharge.find(userbilling.charge_id)
                    if user_charge.status == 'active':
                        return True
                except Exception as e:
                    request.session.flush()
                    create_file = open("requestlogs", "a")
                    create_file.write("usercharge error"+'\n')
                    create_file.close()
                    return -1
    return False

@login_required
def home(request, *args, **kwargs):
    if request.GET.get('shop') != None:
        shop = request.GET.get('shop')
        if shop != request.user.myshopify_domain:
            logout(request)
            request.session.flush()
            return redirect(f"/?shop={shop}")
              
    checkbilling = check_user_billing(request)
    if checkbilling == True:
        return render(request, "home.html")
    if checkbilling == -1:
        return redirect(settings.LOGIN_REDIRECT_URL)
    return redirect(activate_billing)
    
@login_required
def getdata(request, *args, **kwargs):
    if check_user_billing(request)==False:
        return JsonResponse({"status":False,"msg":"You have no active plan."})
    
    if request.method == 'GET' and 'link' in request.GET:

        link=request.GET['link']
			#link="https://"+ link
#			
        if validators.url(link) != True :
            
            return JsonResponse({"status":False,"msg":"URL Invalid, Please put a URL starting with https://","data":[]})


        r = False
        
        
        try :
           r= requests.get(f'{link}.json?limit=250')
        except ConnectionError:
            return JsonResponse({"status":False,"msg":"URL Invalid, Can't find any Product","data":[]})
        
        if r.status_code == 200:
            r=requests.get(f'{link}.json?limit=250')
            with request.user.session:
                c=shopify.CustomCollection.find()
                cJSON=[]
                for cc in c:
                    cJSON.append(cc.to_dict())
                #cm=shopify.SmartCollection.find()
                #for kk in cm:
                #    cJSON.append(kk.to_dict())
#

            rs_obj = {'product': r.json(), 'collections':cJSON }
            return JsonResponse({"status":True,"msg":"",'data':rs_obj})
        else:
            return JsonResponse({"status":False,"msg":"URL invalid or not a shopify store!","data":[]})

    
def getmultidata(request, *args, **kwargs):
    if check_user_billing(request)==False:
        return JsonResponse({"status":False,"msg":"You have no active plan."})
    if request.method == 'GET' and 'linkmulti' in request.GET:
        linkmulti=request.GET['linkmulti']
        if validators.url(linkmulti) != True :
            return JsonResponse({"status":False,"msg":"URL Invalid, Please put a URL starting with https://","data":[]})
        
        
        r = False
        try :
            r= requests.get(f'{linkmulti}/products.json?limit=250&page=1')
            if r.status_code != 200:
                return JsonResponse({"status":False,"msg":"URL Invalid, Not a Shopify store","data":[]})
           
        except ConnectionError :
            return JsonResponse({"status":False,"msg":"URL Invalid, Not a Shopify store","data":[]})
        
        br=[]
        i=1
        stop=True
        while stop==True:
            
            if requests.get(f'{linkmulti}/products.json?limit=250&page={i}').json()['products']==[]:
                stop=False
            else:
                print(f'--------------start-{i}------------------')
                r= requests.get(f'{linkmulti}/products.json?limit=250&page={i}')
                
                print(type(r.json()))
                print(type(br))
                c=r.json()['products']
                br.append(c)
                print(f'--------------end-{i}------------------')
                
            i=i+1

        print('--------------printing product------------------')
        print(br)

        if r.status_code == 200:
            #print(r)
            with request.user.session:
                c=shopify.CustomCollection.find()
                cJSON=[]
                for cc in c:
                    cJSON.append(cc.to_dict())
                cm=shopify.SmartCollection.find()
                for kk in cm:
                    cJSON.append(kk.to_dict())


            rs_obj = {'product': br, 'collections':cJSON }
            return JsonResponse({"status":True,"msg":"",'data':rs_obj})
        
        else:
            return JsonResponse({"status":False,"msg":"url invalid or not a shopify store!","data":[]})

    
    






@login_required
def importoneproduct(request, *args, **kwargs):
    if check_user_billing(request)==False:
        return JsonResponse({"status":False,"msg":"You have no active plan."})
    
    
    if request.method == 'POST':
        body=request.POST
        
        if 'payload' not in body:
            return JsonResponse({"status":False,"msg":"an error occured."})
        
        product = json.loads(body['payload'])
        #print(product['data']['images'])
        with request.user.session:

            #new_product = shopify.Product()

            #print(product['data']['variants'])
            #new_product.title = "Burton Custom Freestyle 151"
            #new_product.product_type = "Snowboard"
            #new_product.vendor = "Burton"
            #success = new_product.save() #returns false if the record is invalid

            #print(product['data']['variants'])
            #print(type(product))
            
            #for x in product['data']['variants']:
            #     del x['id'], x['product_id'], x['position'], x['inventory_policy'], x['compare_at_price'], x['fulfillment_service'], x['inventory_management'], x['created_at'], x['updated_at'], x['taxable']
            #     print(x)
            
            
            
            #for x in product['data']['options']:
            #    del x['id'], x['product_id'], x['position']
                 
            
            
            
            #print(product['data']['options'])
            #print(product['data']['variants'])
            #print(product['data']['options'])
            #product['data']['variants'].pop("id",None)
            #product['data']['variants'].pop("product_id",None)
            #product['data']['variants'].pop("position",None)
            #product['data']['variants'].pop("inventory_policy",None)
            #product['data']['variants'].pop("compare_at_price",None)
            #product['data']['variants'].pop("fulfillment_service",None)
            #print(product['data']['variants'])
            #gen_variants = []
            #a=0
            #for x in product['data']['options']:
            #    a=a+1
            #    vals = x['values']
            #    idx2 = 1
            #    obj = {}
            #    for y in range(len(vals)):
            #        i = y+1
            #        obj[f"option{i}"] = vals[y]
            #        idx2 = idx2 + 1
            #        a=a+1
#
            #    print(obj)
            #    gen_variants.append(obj)
            #    print(gen_variants)         
            #a=0
            #obj = {}
            #gen_variants=[]
            #a=0
            #for i in product['data']['options']:
            #    
            #    for x in product['data']['variants']:
            #       x['values']["option1"] = i['values'][a]
            #       x['values']["option2"] = i['values'][a]
            #    a=a+1
            #    print( x['values'])
            genv={}
            gen_variants=[]
            print('------------')
            for x in product['data']['variants']:
                #del x['barcode'], x['compare_at_price'], x['created_at'], x['fulfillment_service'], x['grams'], x['id'], x['image_id'], x['inventory_management'], x['inventory_policy'], x['inventory_quantity'], x['old_inventory_quantity'], x['position'], x['product_id'], x['requires_shipping'], x['title'],x['price'],x['updated_at'],x['sku'],x['option3'],x['taxable'],x['weight'],x['weight_unit']
                #del x['image_id']
                print(x['inventory_quantity'])
                genv=x
                gen_variants.append(shopify.Variant(x))
            #print(gen_variants)


            
            #obj = {}
            #for x in product['data']['variants']:
            #     obj[f"option1"] = x['option1']
            #     obj[f"option2"] = x['option2']
            #print(obj)
            #
            #print(gen_variants)
            #    
            #    #shopify.Variant({"option1": "Blue", "option2": "L"}),
            #
            
            gen_options=[]
            benbla={}
            for x in product['data']['options']:
                del x['id'], x['product_id'], x['position']
                benbla=x
            
                gen_options.append(shopify.Option(x))
            print(benbla,'dddddd')
            new_product = shopify.Product()
            new_product.title=product['data']['title']
            new_product.body_html=product['data']['body_html']
            new_product.vendor=product['data']['vendor']  
                
            new_product.product_type=product['data']['product_type']
            print(product['data']['options'][0]["values"],'ddddddddddddd')
            #new_product.images=product['data']['images']
            a=product['data']['options'][0]["values"]
            
            #new_product.options = product['data']['options']
            #print(product['data']['options'][1])
#            new_product.variants=gen_variants
            #new_product.options =benbla
            new_product.tags = product['data']['tags']


                    
            if new_product.errors:
                print(new_product.errors.full_messages(),'dddddddssssssspppppppppppspspps')
                a=new_product.errors.full_messages()
                if a.find('following image IDs do not exist'):
                    print('dssssssssssssssssssssssssssssssdddddddddddddd')
                    new_product.variants=[]

                    
    
            #new_product.variants=gen_variants
            sucess=new_product.save()
            if new_product.errors:
                print(new_product.errors.full_messages()) 
            #print(new_product.variants[0].id,'ddddddddd')
            #print(new_product.variants[0])
            default_vrnt=new_product.variants[0].id
            print('ddddddddddddddddd')
            supvar=[]
            
            for c in product['data']['images']:
                new_p_img = shopify.Image();
                new_p_img.product_id = new_product.id
                new_p_img.src = c['src']
                new_p_img.alt = c['alt']
                new_p_img.variant_ids = c['variant_ids'] 
                #print(c)
                sucess = new_p_img.save()
                if new_p_img.errors:
                    print("ddd")
                    print(new_p_img.errors.full_messages()) 
                    print("ddd")
                new_product_id=0
                new_product_id=new_product.id
                for x in product['data']['variants']:
                    
                    if c['id']==x['image_id']:
                        
                        x['image_id']=new_p_img.id
                        new_product_id=new_product.id
                        x['product_id']=new_product.id
                        print(x['image_id'])

                        new_p_variant=shopify.Variant();   
                        print(new_p_variant)                     
                        new_p_variant.product_id=new_product.id
                        new_p_variant.image_id = new_p_img.id
                        new_p_variant.barcode = x['barcode']
                        new_p_variant.compare_at_price = x['compare_at_price']
                        new_p_variant.fulfillment_service = x['fulfillment_service']
                        new_p_variant.grams = x['grams']
                        new_p_variant.inventory_management = x['inventory_management']
                        new_p_variant.inventory_policy = x['inventory_policy']
                        new_p_variant.inventory_quantity = int(x['inventory_quantity'])
                        print(x['inventory_quantity'])
                        new_p_variant.old_inventory_quantity = int(x['old_inventory_quantity'])
                        new_p_variant.option1 = x['option1']
                        new_p_variant.option2 = x['option2']
                        new_p_variant.option3 = x['option3']
                        
                        new_p_variant.price = x['price']
                        new_p_variant.requires_shipping = x['requires_shipping']
                        new_p_variant.sku = x['sku']
                        new_p_variant.taxable = x['taxable']
                        new_p_variant.title = x['title']
                        new_p_variant.weight = x['weight']
                        new_p_variant.weight_unit = x['weight_unit']
                        if new_p_variant.errors:
                            print(new_p_variant.errors.full_messages()) 
        
                        #print(new_p_variant.image_id)
                        #print(supvar)
                        
                        sucess = new_p_variant.save()
                        if new_p_variant.errors:
                            print(new_p_variant.errors.full_messages()) 

                        print(new_p_variant.title)
                        
                        
            for x in product['data']['variants']:
                if  x['image_id']==None:
                        new_p_variant=shopify.Variant();   
                        #print(new_p_variant)          
                        
                        new_p_variant.product_id = new_product.id
                        new_p_variant.title = x['title']
                        new_p_variant.barcode = x['barcode']
                        new_p_variant.compare_at_price = x['compare_at_price']
                        new_p_variant.fulfillment_service = x['fulfillment_service']
                        new_p_variant.grams = x['grams']
                        new_p_variant.inventory_management = x['inventory_management']
                        new_p_variant.inventory_policy = x['inventory_policy']
                        new_p_variant.inventory_quantity = int(x['inventory_quantity'])
                        new_p_variant.old_inventory_quantity = int(x['old_inventory_quantity'])
                        new_p_variant.option1 = x['option1']
                        #new_p_variant.option2 = x['option2']
                        print(x['option1'])
                        print(x)
                        #
                        new_p_variant.option3 = x['option3']
                        new_p_variant.price = x['price']
                        new_p_variant.requires_shipping = x['requires_shipping']
                        new_p_variant.sku = x['sku']
                        new_p_variant.taxable = x['taxable']
                        new_p_variant.weight = x['weight']
                        new_p_variant.weight_unit = x['weight_unit']
                        if new_p_variant.errors:
                            print(new_p_variant.errors.full_messages()) 
                        sucess = new_p_variant.save()
                        if new_p_variant.errors:
                                print(new_p_variant.errors.full_messages()) 

                        print(sucess)
                        print('im here222')
                       
                            
                   
            #for n in product['data']['options']:
            #    print(n)
            #    new_p_option=shopify.Option()  
            #    new_p_option.product_id=new_product.id
            #    new_p_option.name=n['name']
            #    new_p_option.values=n['values']
            #    print('dddqqqqqqqqqqqqqqqqqqq')
            #    if new_p_option.errors:
            #        print(new_p_option.errors.full_messages()) 
            #    sucess = new_p_option.save()
            
            
            
            print('sssssssssssssssss')
            del_var = shopify.Variant.find(default_vrnt)
            print('last kda ma kda',del_var)
            del_var.destroy()
                                     
                        #print(x)
                        #print(sucess)
                        #if new_product.errors:
                        #    print(new_product.errors.full_messages()) 
                        #del x
                
                        

            
                   
            
        return JsonResponse({"status":True,'msg':"everything is good!"})
    return JsonResponse({"status":False,'msg':"Invalid request!"})

from urllib.parse import urlparse
@login_required
def create_product(request, *args, **kwargs):
    if check_user_billing(request)==False:
        return JsonResponse({"status":False,"msg":"You have no active plan."})
    
    if request.method == 'POST':
        body=request.POST
        if 'payload' not in body:
            return JsonResponse({"status":False,'msg':"an error occured"})
        if 'collectionid' not in body:
            return JsonResponse({"status":False,'msg':"an error occured"})
        collid=body['collectionid']
        #print(collid,'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddodododoodo')
        coll=0
        if collid=='':
            coll=0
        else:
            coll=1
        
        product = json.loads(body['payload'])
        oldproducts=json.loads(body['payload'])
        #for x in oldproduct['data']['variants']:
        #    print ('dddddddddddddddddddddd')
        #    print (x)
        with request.user.session:
            #print(request.user.token)
            
            print(oldproducts['data']['variants'])
            a=0
            #print()
            for x in product['data']['variants']:
                if x["image_id"]==None:
                    a=1
                    x['inventory_management']=None
                    x['inventory_policy']='continue'
                    x['fulfillment_service']="manual"
                else:
                    #del x["image_id"],
                    a=2
            
            if a==2:
                product['data']['variants']=[]
                product['data']['images']=[]
                
                
                
                    
                
            print(oldproducts['data']['variants'],"sssssssss")
            #print(product)
            payload = {
              "product": product['data']
            }

            headers = {"Accept": "application/json", "Content-Type": "application/json",'X-Shopify-Access-Token': request.user.token}

            r = requests.post(f"https://{request.user.myshopify_domain}/admin/products.json", json=payload,  headers=headers)
            
                
                
            print(r.json())
            newproid=r.json()
            if coll==1:
                collect = shopify.Collect({ 'product_id': newproid['product']['id'], 'collection_id': collid })
                collect.save()
                

            #print(newproid['product']['id'])
            if a==2:
                    print(newproid['product']['variants'][0]['id'],'dsdsdsdsdsdsdsdsdsdsds')
                    default_vrnt=newproid['product']['variants'][0]['id']
                
                    for c in oldproducts['data']['images']:
                        new_p_img = shopify.Image();
                        new_p_img.product_id = newproid['product']['id']
                        new_p_img.src = c['src']
                        new_p_img.alt = c['alt']
                        new_p_img.variant_ids = c['variant_ids'] 
                        sucess = new_p_img.save()
                        if new_p_img.errors:
                            print(new_p_img.errors.full_messages()) 
                        print(c['id'])
                        
                        for x in oldproducts['data']['variants']:
                            
                            if c['id']==x['image_id']:
                                
                                x['image_id']=new_p_img.id
                                x['product_id']=newproid['product']['id']
        
                                new_p_variant=shopify.Variant();   
                                new_p_variant.product_id=newproid['product']['id']
                                new_p_variant.image_id = new_p_img.id
                                new_p_variant.barcode = x['barcode']
                                new_p_variant.compare_at_price = x['compare_at_price']
                                new_p_variant.fulfillment_service = x['fulfillment_service']
                                new_p_variant.grams = x['grams']
                                new_p_variant.inventory_management = None
                                new_p_variant.inventory_policy = 'continue'
                                new_p_variant.inventory_quantity =x['inventory_quantity']
                                #new_p_variant.old_inventory_quantity = int(x['old_inventory_quantity'])
                                new_p_variant.option1 = x['option1']
                                new_p_variant.option2 = x['option2']
                                new_p_variant.option3 = x['option3']
                                
                                new_p_variant.price = x['price']
                                new_p_variant.requires_shipping = x['requires_shipping']
                                new_p_variant.sku = x['sku']
                                new_p_variant.taxable = x['taxable']
                                new_p_variant.title = x['title']
                                new_p_variant.weight = x['weight']
                                new_p_variant.weight_unit = x['weight_unit']
                                if new_p_variant.errors:
                                    print(new_p_variant.errors.full_messages()) 
                
                                #print(new_p_variant.image_id)
                                #print(supvar)
                                
                                sucess = new_p_variant.save()
                                if new_p_variant.errors:
                                    print(new_p_variant.errors.full_messages()) 
                    del_var = shopify.Variant.find(default_vrnt)
                    print('last kda ma kda',del_var)
                    del_var.destroy()                       


                    
                
                

    return JsonResponse({"status":True,'msg':"Product imported successfully"})
import threading
import asyncio

#@background(schedule=timezone.now())
@login_required
def create_multi_product(request, *args, **kwargs):
        if check_user_billing(request)==False:
            return JsonResponse({"status":False,"msg":"You have no active plan."})

        if request.method == 'POST':
            
            
            #processs killer file
            p_unique_id = '/home/kira/copyproducts/processfolder/'+request.user.myshopify_domain+'.pid'
            if os.path.exists(p_unique_id):
                return JsonResponse({"status":False,"msg":" Please wait till the previous process ends."})

            create_file = open(p_unique_id, "w")
            create_file.write("")
            create_file.close()
            #progress file
            pG_unique_id = '/home/kira/copyproducts/progressfolder/'+request.user.myshopify_domain+'.pid'
            
            
            
            
            body=request.POST
            #link="https://www.beefcakeswimwear.com/"
            #r=requests.get(f'{link}/products.json?limit=250&page=1')    
            
            #multipro=r.json()
            
            if 'payload' not in body:
                return JsonResponse({"status":False,'msg':"an error occured"})
            
            multipro = json.loads(body['payload'])
            oldproducts=json.loads(body['payload'])
           
            
            print(multipro)
            
            a=0
            for x in multipro:
                if os.path.exists(p_unique_id) :
                    filecnt=open(p_unique_id,'r')
                    if filecnt.read()=='STOP':
                        print("stop found")
                        break

                if 'is_checked' in x and  x['is_checked']==True:
                    print(x['is_checked'])
                    print(x['title'])

                    payload = { "product": x }
                    headers = {"Accept": "application/json", "Content-Type": "application/json",'X-Shopify-Access-Token': request.user.token}
                    r = requests.post(f"https://{request.user.myshopify_domain}/admin/products.json", json=payload,  headers=headers)
                    a=a+1
                    create_file_prog = open(pG_unique_id, "w")
                    create_file_prog.write(str(a))
                    create_file_prog.close()
                    print("sucess" ,a ,'+', request.user)
                
                    
            filecnt.close()
            

            if os.path.exists(p_unique_id):
                print("removing pid file")
                os.remove(p_unique_id)     

            sleep(2)
            if os.path.exists(pG_unique_id):
                print("removing progress file")
                os.remove(pG_unique_id)

          
        totalpdt =len(multipro)
        return JsonResponse({"status":True,'msg':f"{a}/{totalpdt} Products imported with success"})

# function to fill the file with stop text
def stop_process(request, *args, **kwargs):
    
    p_unique_id = 'processfolder/'+request.user.myshopify_domain+'.pid'
    if os.path.exists(p_unique_id):
        create_file = open(p_unique_id, "w")
        create_file.write('STOP')
        create_file.close()
    return JsonResponse({"status":True,'msg':"done"})
#threading.Thread(target=create_multi_product).start()

def read_progress(request, *args, **kwargs):
    result=0
    pG_unique_id = 'progressfolder/'+request.user.myshopify_domain+'.pid'
    if os.path.exists(pG_unique_id):
        process_file_read=open(pG_unique_id,'r')
        result=process_file_read.read()
        process_file_read.close()
        return JsonResponse({'progress':int(result)})
    
    return JsonResponse({'msg':""})

def error_404_view(request, exception):
       
    # we add the path to the the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, 'error-404.html')




def logoutview(request):
    logout(request)
    return redirect(home)




























#@login_required
#def importoneproduct(request, *args, **kwargs):
#    if request.method == 'POST':
#        body=request.POST
#        type = body['type']
#        list = json.loads(body['product'])
#        print(list['data']['images'])
#        #body = request.POST.dict()
#        #print(body['product[data][title]'])
#        if 'product'in list:
#            JsonResponse({'error':"goodsssss"})
#        else: 
#            return JsonResponse({'error':"product is none"})
#            
#        #print(request.POST)
#        #data=json.load(request)
#        #product=request.body('product')
#       # posts_serialized = serializers.serialize('json', products)
#        #print(product)
#        return HttpResponse("good")
#    return HttpResponse("no data passed")
#

from django.conf import settings

@login_required
def activate_billing(request, *args, **kwargs):
    if check_user_billing(request) != False:
        return redirect(home)
    with request.user.session:
        application_charge = shopify.RecurringApplicationCharge.create({
                                'name': 'Copy product plan',
                                'price': 2.99,
                                'test': True,
                                'return_url': f'{settings.APP_URL}/handle-charge',
                                'trial_days': 1    
                                })

        return redirect(application_charge.confirmation_url)
        
@login_required
def handle_billing(request, *args, **kwargs):
    if request.method == 'GET' and 'charge_id' in request.GET:
        
        charge_id=request.GET['charge_id']
        with request.user.session:
            activated_charge = shopify.RecurringApplicationCharge.find(charge_id)
            has_been_billed = activated_charge.status == 'active'
            if has_been_billed:
                p = Billing(user=request.user.id,charge_id=activated_charge.id, createdAt=activated_charge.created_at,currentPeriodEnd=activated_charge.billing_on)
                p.save()

                
                return redirect(home)

    return render(request,"error-403.html")





def privacyPview(request, *args, **kwargs):
       
    return render(request, 'privacy-policy.html')


from django.views.decorators.csrf import csrf_exempt
import hashlib, base64, hmac
def verifysignature(request):
    create_file = open("requestlogs", "a")
    create_file.write(request.body.decode('utf-8')+'\n')
    create_file.close()
    hmac_to_verify    = request.META['HTTP_X_SHOPIFY_HMAC_SHA256'] if 'HTTP_X_SHOPIFY_HMAC_SHA256' in request.META else None
    body=request.body
    hash = hmac.new(settings.SHOPIFY_APP_API_SECRET.encode('utf-8'), body, hashlib.sha256)
    hmaca= base64.b64encode(hash.digest()).decode()
    return hmaca==hmac_to_verify
    
    
@csrf_exempt
def gdprCustomerdatarequest(request, *args, **kwargs):
    if verifysignature(request) != True:
        return JsonResponse({},status=403)
    return JsonResponse({},status=200)

@csrf_exempt  
def customerErasurendpoint(request, *args, **kwargs):
    if verifysignature(request) != True:
        return JsonResponse({},status=403)
    return JsonResponse({},status=200)
 

@csrf_exempt
def shopErasurendpoint(request, *args, **kwargs):
    if verifysignature(request) != True:
        return JsonResponse({},status=403)
    
    data = json.loads(request.body.decode('utf-8')) 
    p=AuthAppShopUser.objects.filter(myshopify_domain=data.shop_domain)
    for user in p:
         a=Billing.objects.get(user=user.id)
         a.delete()

    
    return JsonResponse(status=200)
 

     
