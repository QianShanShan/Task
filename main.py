import requests
import csv
from lxml import etree
class Get_Data():
    def __init__(self):
        self.url = 'https://gpt.candobear.com/prompt'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        self.f = open('data.csv', 'w', encoding='utf-8', newline='')
        self.witer = csv.writer(self.f)
        self.witer.writerow(['标题','详情页url','图片url','类型','关键字','星级','作者'])
        self.data_list = []

    def get_res(self):
        '''
        发送请求，获得网页内容
        :return: res
        '''
        response = requests.get(url=self.url,headers=self.headers)
        res = response.text
        return res
    def parse(self,res):
        '''
        解析获得数据
        :param res: 网页文本
        :return:
        '''
        # 匿名函数 补全获得的url，如果没有获得到数据则返回 -
        get_url = lambda x:'https://gpt.candobear.com/'+x[0] if x else '-'
        # 匿名函数 将获取到的列表中数据转成字符穿，如果没有获得到数据则返回 -
        get_str = lambda x:','.join(x) if x else '-'
        tree = etree.HTML(res)
        # 获取到包含所有信息的div列表，每一个div代表一个模块
        div_list = tree.xpath('//div[@class="notion-collection-gallery medium"]/div')
        for div in div_list:
            # 创建一个列表用来装每一次获取到的数据
            da_list = []
            # 获取标题，并存入列表中
            ti = div.xpath('./div[@class="notion-collection-card__content"]/div[@class="notion-property notion-property__title"]//text()')
            title = get_str(ti)
            da_list.append(title)
            # 获取详情页面url，并存入列表中
            uri = div.xpath('./a/@href')
            url = get_url(uri)
            da_list.append(url)
            # 获取图片url，并存入列表中
            img_uri = div.xpath('./div[@class="notion-collection-card__cover medium"]/span/noscript/img/@src')
            img_url = get_url(img_uri)
            da_list.append(img_url)
            # 获取类型，并存入列表中
            kind = div.xpath('./div[@class="notion-collection-card__content"]/div[@class="notion-collection-card__property-list"]//div[@class="notion-property notion-property__select property-574c4b3f"]//text()')
            kind = get_str(kind)
            da_list.append(kind)
            # 获取关键词，并存入列表中
            keywords = div.xpath('./div[@class="notion-collection-card__content"]/div[@class="notion-collection-card__property-list"]//div[@class="notion-property notion-property__select property-3e415c42"]//text()')
            keywords = get_str(keywords)
            da_list.append(keywords)
            # 获取星级，并存入列表中
            star = div.xpath('./div[@class="notion-collection-card__content"]/div[@class="notion-collection-card__property-list"]//div[@class="notion-property notion-property__select property-5f6b4b7e"]//text()')
            star = get_str(star)
            da_list.append(star)
            # 获取作者，并存入列表中
            author = div.xpath('./div[@class="notion-collection-card__content"]/div[@class="notion-collection-card__property-list"]//div[@class="notion-property notion-property__person property-3e7d4b6b"]//text()')
            author = get_str(author)
            da_list.append(author)
            # 将每一次获取的数据存入self.data_list
            self.data_list.append(da_list)

    def save(self,data):
        '''
        存储数据
        :param data: 列表数据
        :return:
        '''
        self.witer.writerow(data)


    def main(self):
        res = self.get_res()
        self.parse(res)
        for i in self.data_list:
            self.save(i)
    def __del__(self):
        self.f.close()

if __name__ == '__main__':
    Get_Data().main()