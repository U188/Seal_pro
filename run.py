import requests ,re ,base64 ,datetime ,time ,os ,send #line:1
def seal ():#line:2
    O0OOOOO0000O0OO00 =requests .post (url ='http://api.sealnet.cf:8080/seal/getSsrLines',data ={'seed':(None ,'983376297')})#line:3
    try :#line:4
        if O0OOOOO0000O0OO00 .status_code ==200 :#line:5
            return O0OOOOO0000O0OO00 .json ()['data']#line:6
    except Exception as O0OO0O00OO0OOO000 :#line:7
        print (O0OO0O00OO0OOO000 )#line:8
def main ():#line:9
    OO0O00000O0O0O000 =seal ()#line:10
    OOOO0O0O000O00OO0 =''#line:11
    O0OOO0OOOO0O0OO0O ='https://www.ssleye.com/des/web_aes_decrypt'#line:12
    OOOO0OOOO0O0O0O0O ={'Cookie':'CNZZDATA1274973651=1263393379-1608735326-%7C1610152177; his=a%3A1%3A%7Bi%3A0%3Bi%3A170%3B%7D; UM_distinctid=176e48c708f440-00d38ca8292262-7437877-5a900-176e48c70903b2'}#line:15
    O0OOOO0O00OO0000O ={'text':OO0O00000O0O0O000 ,'encode_flag':'utf8','key':'eaddnwdnagdjadwe','iv':'','mode':'ECB','padding':'zero','out_mode':'base64'}#line:24
    try :#line:25
        OO000OO0O0OOOO000 =requests .post (O0OOO0OOOO0O0OO0O ,headers =OOOO0OOOO0O0O0O0O ,data =O0OOOO0O00OO0000O ).text #line:26
        O00O0OOO0OO00OO0O =re .findall (r'(?<=\"\>\<pre\>\[{).+(?=}])',OO000OO0O0OOOO000 .replace ('&#34;',''))[0 ]#line:28
        O00O0OOO0OO00OO0O =O00O0OOO0OO00OO0O .split ('},{')#line:29
        for OOO0O0O0O0OOO000O in O00O0OOO0OO00OO0O :#line:30
            O00O00OO0OO00OO0O =re .findall (r'(?<=name:).+(?=,host)',OOO0O0O0O0OOO000O )[0 ]#line:31
            O00O0O0OO0OOOOO00 =re .findall (r'(?<=host:).+(?=,port)',OOO0O0O0O0OOO000O )[0 ]#line:32
            OO0O0O0O0O00O00O0 =re .findall (r'(?<=port:).+(?=,passw)',OOO0O0O0O0OOO000O )[0 ]#line:33
            OO0O00O0OO0000OO0 =re .findall (r'(?<=obfs:).+(?=,auths)',OOO0O0O0O0OOO000O )[0 ]#line:34
            OO00000OO00O000O0 =re .findall (r'(?<=protocol:).+(?=,obfspa)',OOO0O0O0O0OOO000O )[0 ]#line:35
            OOO000OOOO0OOO000 =re .findall (r'(?<=password:).+(?=,obfs:plain)',OOO0O0O0O0OOO000O )[0 ]#line:36
            OO00OO00OOO0O0O00 =O00O0O0OO0OOOOO00 +':'+OO0O0O0O0O00O00O0 +':'+OO00000OO00O000O0 +':none:'+OO0O00O0OO0000OO0 +':'+base64 .b64encode (OOO000OOOO0OOO000 .encode ('utf-8')).decode ()+'/?remarks='+base64 .b64encode (O00O00OO0OO00OO0O .encode ('utf-8')).decode ()+'&protoplasm=&obfsparam='#line:39
            OOO0O00O00000O000 ='ssr://'+base64 .b64encode (OO00OO00OOO0O0O00 .encode ('utf-8')).decode ()#line:41
            with open (str (datetime .date .today ())+'.txt','a')as OOO0O000000OO00OO :#line:42
                OOO0O000000OO00OO .write (OOO0O00O00000O000 +'\n')#line:43
    except Exception as O0OOO00000OO00O00 :#line:46
        print (O0OOO00000OO00O00 )#line:47
if __name__ =='__main__':#line:49
    main ()#line:50
    time .sleep (2 )#line:51
    send .send_email ()
