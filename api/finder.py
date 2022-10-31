from http.server import BaseHTTPRequestHandler
from nis import cat
import requests
from urllib import parse 

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        s = self.path
        response = ''
        base_url =  'https://restcountries.com/v3.1/'
        url_components=parse.urlsplit(s)
        query_params =  dict(parse.parse_qsl(url_components.query))
        country = query_params.get('country')
        capital = query_params.get('capital')


        if not country and not capital:
            self.send_response(404)
            self.send_header('Content-type','text/plain')
            self.end_headers()         
            self.wfile.write('Please Provide country or captial'.encode())
            return
        
        if country:
            url = base_url + f'name/{country}'
            response = f'The capital of {country} is '
        else:
            url = base_url + f'capital/{capital}'
            response = f'{capital} is the capital of '
        try:
            print(url)
            r = requests.get(url)
             
            
            capital_name = r.json()[0]['capital'][0]
            country_name = r.json()[0]['name']['common']
            print(capital_name,country_name)
            response = response + capital_name if country else response + country_name
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers() 
        except Exception as e:
            print(e)
            response = f'Sorry, we didnt find results for {country or capital}'
            self.send_response(404)
            self.send_header('Content-type','text/plain')
            self.end_headers() 
        finally:
            self.wfile.write(response.encode())
            return