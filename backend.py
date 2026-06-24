

import requests




    


def main(pname):
    url=f"https://pokeapi.co/api/v2/pokemon/{pname}"
    
    data=requests.get(url)
    if(data.status_code==200):
        signal="green"
        
        response=data.json()
        image_url=response.get('sprites', {}).get('other', {}).get('official-artwork', {}).get('front_default')
        idd=response.get('id')

        hight=response.get('height')
        weight=response.get('weight')/10
        return signal,idd,weight,hight,image_url


    elif(data.status_code==404):
        signal="red"
        idd=None
        weight=None
        hight=None
        image_url=None
        return signal,idd,weight,hight,image_url
    else:
        signal="black"
        idd=None
        weight=None
        hight=None
        image_url=None
        return signal,idd,weight,hight,image_url