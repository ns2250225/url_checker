# -*- coding: utf-8 -*-
import os.path

import requests

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', res=[], flag=0)

    def post(self):
        urls = self.get_argument('urls')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        }
        res = []
        resp = ""
        if not urls:
            self.render('index.html', res=[{"error_url": "无", "status_code": 0, "reason": "url列表为空"}], flag=0)
            return False
            
        for url in urls.split('\n'):
            tmp_url = url.strip()
            print(tmp_url)
            try:
                resp = requests.get(tmp_url, headers=headers, timeout=8, verify=False)
                if resp.status_code == requests.codes.ok:
                    print("ok")
                else:
                    print("fail: {}".format(resp.status_code))
                    res.append({
                        "error_url": url,
                        "status_code": resp.status_code,
                        "reason": "连接超时，可能是网络问题或URL地址错误"
                    })
            except:
                print("error: {}".format(url))
                res.append({
                    "error_url": url,
                    "status_code": 500,
                    "reason": "服务器没响应，可能链接死了，请及时确认"
                })
        self.render('index.html', res=res, flag=0)




if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/', IndexHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=False
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(int(options.port), "0.0.0.0")
    http_server.start(0)
    # http_server.listen(8000)
    tornado.ioloop.IOLoop.current().start()
