# -*- coding:utf8 -*-
from pyogp import pyogp
from pyogp.get_image import ImageExtractor
import unittest
from pyogp.decorators import print_running_time
from pyogp.cache import mysqlcache

from urlparse import urljoin


class TestCase(unittest.TestCase):

    def setUp(self):
        self.required_set = {'title', 'image', 'description'}  # set literal

    def tearDown(self):
        pass

    @print_running_time
    def test_naver_blog(self):
        """
        frame -> ogp
        """
        url = "http://blog.naver.com/mjl0906/220310129634"
        result = pyogp.PyOGP(
            required_set=self.required_set).crawl(url).result
        target_image = "http://blogthumb2.naver.net/20150324_148/"\
                         "mjl0906_1427204642008cXM71_JPEG/926870_962186357140505_1898497724_n.jpg?type=w2"
        self.assertEqual(target_image, result['image'])
        self.assertIn(u'민쥬왕국/얼짱/장다연', result['title'])
        

    @print_running_time
    def test_wordPressBlog(self):
        """
        observe ogp
        """
        url = "http://sungmooncho.com/2015/03/15/what-makes-a-great-product-great/"
        result = pyogp.PyOGP(required_set=self.required_set).crawl(url).result
        target_image = "https://sungmoon.files.wordpress.com/2015/03/virginamerica.jpg"
        self.assertEqual(target_image, result['image'])
        self.assertEqual(set(result.viewkeys()), self.required_set)

    @print_running_time
    def test_case_1(self):
        """
        not ogp
        본문에도 적당한 image 없다
        <meta name="description" content="foo">
        <title></title>
        :return:
        """
        url = "http://www.siafoo.net/article/52"
        result = pyogp.PyOGP(required_set={'title', 'description'}).crawl(url).result
        self.assertEqual(set(result.viewkeys()), {'title', 'description'})

    @print_running_time
    def test_case_2(self):
        """
        og:image
        <meta property="og:image" content="/img/apple-touch-icon.png">
        <meta name="description" content="foo">
        <title></title>
        og:img에 /img/apple-touch-icon.png로 이상함
        :return:
        """
        url = "http://m.biz.chosun.com/svc/article.html?contid=2015032702011&facebook"
        result = pyogp.PyOGP(required_set=self.required_set).crawl(url).result
        self.assertEqual(set(result.viewkeys()), self.required_set)

    @print_running_time
    def test_case_3(self):
        """
        og:image
        og:title
        <meta itemprop="description" name="description" content="스타트업(초기기업..">
        <meta property="og:image" content = ""> content에 ""빈껍데기를 둔 놈들 다 몽둥이로 맞아야함

        :return:
        """
        url = "http://m.mt.co.kr/renew/view.html?no=2015042014305194647"
        result = pyogp.PyOGP(required_set=self.required_set).crawl(url).result
        # iamge 가져오기로 가져와야할 이미지
        target_image = "http://thumb.mt.co.kr/06/2015/04/2015042014305194647_1.jpg"
        self.assertEqual(set(result.viewkeys()), {'title', 'description'})
        # get_image.py적용
        img_list = ImageExtractor(origin=url).get_image()
        ranked_list = ImageExtractor().image_rank(img_list)
        scraped_image = ranked_list[0][0]
        self.assertEqual(scraped_image, target_image)

    @print_running_time
    def test_case_4(self):
        """
        the num of og:description : 2
        the lower part meta info is correct
        나중에 오지 디스크립션이 이렇게 두개인경우 본문이랑 비교해서 골라주는 것을 생각할 수도 있음
        :return:
        """
        url = "http://sisareport.com/1%EB%B6%84%EA%B8%B0-%EC%B1%84%EC%9A%A9%EA%B3%B5"\
            "%EA%B3%A0-%E3%80%8C%EA%B2%BD%EB%A0%A5%EC%9D%B4-%EC%8B%A0%EC%9E%85%EC%9D%98-4-6%EB%B0%B0%E3%80%8D/"
        result = pyogp.PyOGP(required_set=self.required_set).crawl(url).result
        self.assertEqual(set(result.viewkeys()), self.required_set)

    @print_running_time
    def test_db_cache(self):
        """
        mysql cache db 생성 테스트
        """
        ogp = pyogp.PyOGP()
        mysqlcache.MySQLCache.init_app(ogp,
                                       host='pongpongpong.cbmdsp0culle.us-west-2.rds.amazonaws.com',
                                       user='pongpongpong',
                                       passwd='pongpongpong')

        ogp.crawl('http://www.naver.com')
        ogp.crawl('http://www.naver.com')
        cur = ogp.cache.conn.cursor()
        cur.execute('select * from {}'.format('ogp_cache.ogp_cache'))
        self.assertEqual(cur.rowcount, 1)
        cur.close()



if __name__ == '__main__':
    unittest.main()
