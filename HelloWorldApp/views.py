# Create your views here.
from django.http import HttpResponse
import requests
import sqlite3


def foo(request):
    url = 'https://api.clicky.com/api/stats/4?site_id=100716069&sitekey=93c104e29de28bd9&type=visitors-list'
    date = '&date=2016-05-18'
    limit = '&limit=all'
    output = '&output=json'
    # nyu = '&ip_address=59.79.127.0,59.79.127.255|91.230.41.0,91.230.41.255|94.56.130.144,94.56.130.159|94.56.170.16,94.56.170.31|94.200.220.160,94.200.220.191|101.231.120.128,101.231.120.159|103.242.128.0,103.242.131.255|128.122.0.0,128.122.255.255|128.238.0.0,128.238.255.255|176.74.48.32,176.74.48.63|180.169.77.32,180.169.77.63|192.76.177.0,192.76.177.255|192.86.139.0,192.86.139.255|192.114.110.0,192.114.110.255|193.175.54.0,193.175.54.255|193.205.158.0,193.205.158.128|193.206.104.0,193.206.104.255|194.214.81.0,194.214.81.255|195.113.94.0,195.113.94.255|195.229.110.0,195.229.110.191|198.71.44.128,198.71.44.191|202.66.2.16,202.66.2.31|202.66.60.160,202.66.60.191|203.174.165.128,203.174.165.255|212.219.93.0,212.219.93.255|213.42.147.0,213.42.147.63|216.165.0.0,216.165.127.255'
    r = requests.get(url+date+limit+output)
    # print(url+date+limit+output+nyu)
    data = r.json()
    html = []
    for item in data[0]['dates'][0]['items']:
        ip = item["ip_address"]
        si = item["session_id"]
        org = item["organization"]
        html.append("<tr><td>%s</td><td>IP_Address</td><td>%s</td><td>Session_ID</td><td>%s</td></tr>" %(org, ip, si))
        conn = sqlite3.connect("/Users/arifshaikh/JomiAnalytics/pythonsqlite.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS xjomi
                              (org text, ip text, si text)
                           """)
        varhtml = []
        varhtml = [(org, ip, si)]
        cursor.executemany("INSERT INTO xjomi VALUES (?,?,?)", varhtml)
        conn.commit()
    return HttpResponse('<table>%s</table>' % '\n'.join(html))




    # import urllib
    # print(url + nyu + urllib.urlencode(getVars))
