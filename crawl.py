# 获取问卷星中所有问卷数据
# 通过post请求能够获取数据
import requests
import json
import re
import time

from bs4 import BeautifulSoup

def get_qas(html):
    # new_url = url+ token
    # html = get_html(new_url)
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        title = soup.find('div', attrs={'id':'toptitle'}).text.strip()
    except Exception as e:
        print(str(e))
        return 0
    else:
        comment = soup.find('div', attrs={'class':'topic__type-des'})
        if comment:
            comment = comment.text.strip()
        all_element = soup.find_all('div', attrs={'class':'topic__type-body'})[0]
        qas = []
        for element in all_element.find_all('fieldset'):
            # print(element)
            question = element.find('legend', attrs={'class':'topic__type-title'})
            if not question:
                continue

            question = question.text
            print(question)
            # question = re.findall("<legend class=\"(.*)\">(.*?)：</legend>", str(element))
            # print(question)
            options_ele = element.find('div', attrs={'class':'topic__type-dry'})
            options = []
            if not options_ele:
                continue
            for ele in options_ele:
                option = re.findall("<label>(.*?)</label>", str(ele))
                if option:
                    option = option[0]
                options.append(option)
            qas.append({"q": question, "options": options})
            
        result = {"title": title, "comment": comment, "qa": qas}
        return result

def get_response(index):
    url = "https://www.wjx.cn/xz/{}.aspx".format(index) + "?u_atoken=64f1b01f-dce4-450a-b54b-c170896efdbf&u_asession=01c_3r2TXrhB7MYbqkG7N01MGqhLo7qEME2AwWh6xd9Hzi_pA4Cwv0tIAnCnmcL6PQX0KNBwm7Lovlpxjd_P_q4JsKWYrT3W_NKPr8w6oU7K_5fDtW5_A3DF6uTbrost6bGALgmy0OhKJ6h8uIjom8j2BkFo3NEHBv0PZUm6pbxQU&u_asig=05eSL-lwKzeCrURTCAYI4JXlClUTB-BQMd1NEPiTxKwSheipInjjzmjA8XY_T88_5NjKYbiZ_SI0RFtAsGT0AYZqckqsX4b2zG647AFm87vKkLGReLE5Q_oHQupZ3H3vPiDgTsdkCc31QfYbOn-4CuE6ViXT_4dK4JNBBYNszOQI39JS7q8ZD7Xtz2Ly-b0kmuyAKRFSVJkkdwVUnyHAIJzQHmOcNRYTQJ5QW58kKixrnDutHMZiek1Pe91QB0PgMlBMZyRAui7XvSM8Ig_GQPYO3h9VXwMyh6PgyDIVSG1W__Usb2_e4Bo6yPIVCbAzttGUOQ9o1DH5jrMNt2rYW_5AheDzJXF6VQ4BA6hJAVGy4kMNx4_KHY1phD_WIOThtUmWspDxyAEEo4kbsryBKb9Q&u_aref=gPmtIz378BPnmJUCPgppzs62Fhk%3D"
    headers = {
            "Content-Type": "text/html; charset=utf-8",
            "Referer": "https://www.wjx.cn/newwjx/mysojump/newselecttemplete.aspx?",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "Cookie": ".ASPXANONYMOUS=7v_dCLBz2QEkAAAAMTVkODYxNmQtMWZhNi00NzQ3LTgyM2UtZDNhZWYwYmEzMTJku5Oy6Q16L4xgS39AGxeeSv1S9Dw1; _uab_collina=167601279092441877513722; Hm_lvt_21be24c80829bd7a683b2c536fcf520b=1678414745; Hm_lpvt_21be24c80829bd7a683b2c536fcf520b=1678415654; acw_tc=707c9fd316784368576703572e5dac7e25644331c0da6ad733419856627a63; acw_sc__v3=640aea06e5775fb477a180622c24713f7f710f1c; SERVERID=797658896bbfe7476f5f4103a02a2b4f|1678436891|1678436873; ssxmod_itna=Yqjh7KYKBKGIIDfxBad=TmPDv9hjxmTKDQWom7DlpixA5D8D6DQeGTTR=kEqmqrY6OhfG50lGmfimWbBvfP/WxWaXoD84i7DKqibDCqD1D3qDkT9Qxii9DCeDIDWeDiDGR8D0pyQODjivzlrK17pDGDlWzmxFCncDDUmDDEA+kDl9pDCFsnPKHizvGZ=ge5AnETnw8r0+4+nDosn0edjieeeMq5=04hBuD5CiYeGhf5T4DiPR2oYD===; ssxmod_itna2=Yqjh7KYKBKGIIDfxBad=TmPDv9hjxmTKDQWomD6ptj6D0HeY03ru60muS=XSduSEduQ7qIp0FA7yt4L26eYoZ8u=AezxCGWWEDQKaDLxiQb4D==="
            } 
    response = requests.get(url, headers=headers)
    response.encoding='utf-8'
    return response

def select_begin_point(begin_index):
    # sleep之后需要再次请求，选择一个合适的开始位置，index 每10个一试，最后要么10个都不行，要么有可行的
    print("开始选择：", begin_index)
    index = begin_index
    cnt = 0
    qas = 0
    while (not qas) and (cnt < 20):
        cnt = cnt + 1
        html = get_response(index)
        qas = get_qas(html.text)
        print(html.text)
        index = index + 10
    
    print("结束选择：", index - 10)
    return index - 10
     
def formatted_questionaries(begin_index):
    index = select_begin_point(begin_index)
    print("index: ", index)
    cnt = 0
    while True:
        html = get_response(index)
        qas = get_qas(html.text)
        print("qas:", qas)
        if qas:
            qas["url"] = "https://www.wjx.cn/xz/{}.aspx".format(index)
            with open('./crawl/wenjuanxing_final_5.json', "a") as f:
                json.dump(qas, f, ensure_ascii=False)
                f.write(",")
                f.close()
            # 继续挖掘下一个
            index = index + 1
            # 重新计数
            cnt = 0
        else:
            if cnt < 20:
                # 不是中断
                index = index + 1
                cnt = cnt + 1
            else:
                # 中断需要
                print("开始sleep: ")
                time.sleep(480)
                print("结束sleep: ")
                index = select_begin_point(index)


formatted_questionaries(209451158)