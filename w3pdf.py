import pdfkit
import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import os
from PyPDF2 import PdfFileMerger
import shutil

config = pdfkit.configuration(wkhtmltopdf=r'J:\wkhtmltopdf\bin\wkhtmltopdf.exe')

siteURL = "http://www.pbr-book.org/3ed-2018/contents.html"
siteBaseURL = "http://www.pbr-book.org/3ed-2018/"

resp = requests.get(siteURL)
http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
encoding = html_encoding or http_encoding
soup = BeautifulSoup(resp.content, from_encoding=encoding)

for link in soup.find_all('a',href=True):
    if "https" in link:
        continue
    else:
        urlList.append(link['href'])

x = 0
os.mkdir('output')
for page in urlList:
    if "contents" in page or "#" in page or "patreon" in page:
        continue
    tempURL = siteBaseURL + page
    print(tempURL)
    tempFile = str(x) + ".pdf"
    tempFile = os.path.join("output",tempFile)
    pdfkit.from_url(tempURL, tempFile, configuration=config)
    x += 1

fileList = os.listdir("output")
fileList.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
merger = PdfFileMerger()
shutil.rmtree("output")
for pdf in fileList:
    tempFile = "output\\" + pdf
    merger.append(tempFile, import_bookmarks=False)

merger.write("final.pdf")
