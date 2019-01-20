import requests
from time import sleep
import csv
import pdb

class AllegroCore:

    def __init__(self, mode='REGULAR', search_type='Product', fallback="false"):

        self.token=None
        self.mode=mode
        self.search_type=search_type
        self.base='https://allegro.pl'
        self.client_id='2458f8b445a942cc9af5fdc3da846766'
        self.client_secret='7jYFAwixGWdZO1TBc0lJAie4PkSd5Uw4YlCjamNsvw6KGxsRw5wGeXG4dkaFF6Fs'
        self.items=[]#list of dictionary of search items
        self.row_count=0
        self.fallback=fallback
        self.fifty_check=True

    def get_verification_url(self):
        url=self.base+'/auth/oauth/device'
        headers = {
            'Authorization': "Basic MjQ1OGY4YjQ0NWE5NDJjYzlhZjVmZGMzZGE4NDY3NjY6N2pZRkF3aXhHV2RaTzFUQmMwbEpBaWU0UGtTZDVVdzRZbENqYW1Oc3Z3NktHeHNSdzV3R2VYRzRka2FGRjZGcw==",
            'Content-Type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache",
        }
        payload = "client_id="+self.client_id
        response = requests.request("POST", url, data=payload, headers=headers)
        resjson=response.json()
        self.device_code=resjson['device_code']
        return response.json()

        #TODO: show verification_url and user_code to user


    def chk_if_verified(self, device_code):
        url = "https://allegro.pl/auth/oauth/token"

        querystring = {"grant_type": "urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Adevice_code",
                       "device_code": device_code}

        payload = ""
        headers = {
            'Authorization': "Basic MjQ1OGY4YjQ0NWE5NDJjYzlhZjVmZGMzZGE4NDY3NjY6N2pZRkF3aXhHV2RaTzFUQmMwbEpBaWU0UGtTZDVVdzRZbENqYW1Oc3Z3NktHeHNSdzV3R2VYRzRka2FGRjZGcw==",
            'cache-control': "no-cache",
        }

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
        json_response = response.json()
        if response.status_code == 200:
            self.token=json_response['access_token']
        return response.status_code



    def get_token(self):
        url = "https://allegro.pl/auth/oauth/token"
        querystring = {"grant_type": "client_credentials"}
        payload = ""
        headers = {
            'Authorization': "Basic MjQ1OGY4YjQ0NWE5NDJjYzlhZjVmZGMzZGE4NDY3NjY6N2pZRkF3aXhHV2RaTzFUQmMwbEpBaWU0UGtTZDVVdzRZbENqYW1Oc3Z3NktHeHNSdzV3R2VYRzRka2FGRjZGcw==",
            'cache-control': "no-cache",
        }
        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
        self.token=response.json()['access_token']
        return self.token

    def search(self, phrase):
        if len(phrase) > 50 :
            if self.fifty_check==True:
                phrase=phrase[:50]
        url='https://api.allegro.pl/offers/listing?phrase='+phrase+'&searchMode='+self.mode+'&fallback='+self.fallback
        res=requests.get(url,headers={'content-type':'application/vnd.allegro.public.v1+json', 'Authorization':'Bearer '+self.token, 'Accept':'application/vnd.allegro.public.v1+json'})
        response_json=res.json()
        if res.status_code == 200:
            promoted=response_json['items']['promoted']
            regular=response_json['items']['regular']
            self.write_to_excel(promoted, regular)


    def poll_verification(self):
        count=0
        while True:
            status_code=self.chk_if_verified(self.device_code)
            if status_code == 200 :
                return True
            sleep(3)
            if count > 200 :
                return False
            count = count + 1


    def read_excel2(self, input_file):
        data_df=''#pd.read_csv(input_file, encoding='latin-1')
        for index , row in data_df.iterrows():
            new_item = {'EAN': row['EAN'], 'BUY PRICE': row['Price'], 'Product': row['Product'],
                        'Number': row['Number']}
            self.items.append(new_item)
            print(new_item)



    def read_excel3(self, input_file):

       with open(input_file, encoding='latin-1') as csv_file:
            #csv_reader=csv.DictReader(csv_file)
            csv_reader=''#UnicodeDictReader(csv_file)
            for row in csv_reader:
                new_item={'EAN':row['EAN'], 'BUY PRICE':row['Price'], 'Product':row['Product'], 'Number':row['Number']}
                self.items.append(new_item)
                print(new_item)
       return True

    def read_excel(self, input_file='input.csv'):
        with open(input_file, encoding='latin-1') as csv_file:
            file=csv_file.read()

            rows=file.split('\n')
            for row in rows[1:]:
                double_quote_index1=row.find('"')
                if double_quote_index1 != -1:
                    new_string=row[(double_quote_index1+1):]
                    double_quote_index=new_string.index('"')
                    new_string=new_string[0:double_quote_index]
                    new_string=new_string.replace(';', '')
                    replace_string=row[double_quote_index1:(double_quote_index1+double_quote_index+2)]
                    row=row.replace(replace_string,new_string)

                row_list=row.split(';')
                try:
                    new_item = {'EAN': row_list[1], 'BUY PRICE': row_list[3].replace(',','.'), 'Product': row_list[2],
                                'Number': row_list[0]}
                except IndexError:
                    continue

                self.items.append(new_item)






    def start_search(self):
        print('start here --- ' )
        self.count=1
        for item in self.items:
            self.item = item
            self.search(item[self.search_type])
            print(str(self.count)+' Done with - >'+self.search_type  +' -> '+item['Product'])
            self.count+=1
        return True


    def write_row(self, output, cate):
        try:
            sell_price = output['sellingMode']['price']['amount']
        except:
            sell_price='not found'
        try:
            image_url = output['images'][0]['url']
        except:
            image_url='not found'
        try:
            lowest_shipping = output['delivery']['lowestPrice']['amount']
        except:
            lowest_shipping='not found'
        try:
            popularity=output['sellingMode']['popularity']
        except:
            popularity='not found'
        try:
            available=output['delivery']['availableForFree']
        except:
            available='not found'
        try:
            seller_id=output['seller']['id']
        except:
            seller_id='not found'
        try:
            id=output['id']
        except:
            id='not found'
        try:
            stock=output['stock']['available']
        except:
            stock='not found'
        try:
            format=output['sellingMode']['format']
        except:
            format='not found'
        try:
            name=output['name']
        except:
            name='not found'



        #pdb.set_trace()
        row = [self.item['Number'], self.item['EAN'], name,self.item['BUY PRICE'], image_url, '',sell_price, popularity,
               cate
            , lowest_shipping, available, seller_id, id
            , stock, format
        ]
        self.row_count+=1
        return row

    def write_to_excel(self, promoted, regular):
        len=promoted.__len__()+regular.__len__()
        with open('output.csv', mode='a', encoding='utf-8') as output_file:
            output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            row=[self.item['Number'],self.item['EAN'], self.item['Product'],self.item['BUY PRICE'],'',len]
            self.row_count+=1
            output_writer.writerow(row)
            for output in promoted:
                try:
                    row=self.write_row(output,'promoted')
                    output_writer.writerow(row)
                except:
                    print(output)
            for output in regular:
                try:
                    row=self.write_row(output, 'regular')
                    output_writer.writerow(row)
                except:
                    print(output)



























