import mitmproxy.http
import re
import os
import tempfile
if os.name=="nt":
    executefile="n-m3u8dl-re.exe"
else:
    executefile="n-m3u8dl-re"
def response(flow:mitmproxy.http.HTTPFlow):
    #如果域名匹配"dtliving-*.dingtalk.com"
    if flow.request.method=="GET" and re.match(r'dtliving-.+\.dingtalk\.com',flow.request.host) and re.match(
            r"/live_hp/([a-zA-Z0-9-]+)_normal\.m3u8\?auth_key=([a-zA-Z0-9-]+)",flow.request.path):
        #将内容写入到tempfile获取的临时文件地址，每次覆盖写入，如果文件不存在则创建
        tmpfile_path=tempfile.mkstemp(".m3u8","dingtalk-live-downloader")[1]
        with open(tmpfile_path,"w+") as f:
             f.write(flow.response.content.decode("utf-8"))
        #调用n-m3u8dl-re-bin下载。
        os.system(executefile+r" "+tmpfile_path+" --base-url https://"+flow.request.host+r"/live_hp/ --save-dir . --save-name "+re.match(
            r"/live_hp/([a-zA-Z0-9-]+)_normal\.m3u8\?auth_key=([a-zA-Z0-9-]+)",flow.request.path).group(1)+r".mp4 --no-log ")
        #删除临时文件
        os.remove(tmpfile_path)