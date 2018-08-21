# [Scrapy中CSS用法介绍](https://www.cnblogs.com/zhaof/p/7189860.html)

　　Scrapy提取数据有自己的一套机制，被称作选择器（selectors）,通过特定的Xpath或者CSS表达式来选择HTML文件的某个部分  
　　Xpath是专门在XML文件中选择节点的语言，也可以用在HTML上。
CSS是一门将HTML文档样式化语言，选择器由它定义，并与特定的HTML元素的样式相关联。

#### XPath选择器

　　常用的路径表达式，这里列举了一些常用的，XPath的功能非常强大，内含超过100个的内建函数。
下面为常用的方法

    nodeName    选取此节点的所有节点
    /           从根节点选取
    //          从匹配选择的当前节点选择文档中的节点，不考虑它们的位置
    .           选择当前节点
    ..          选取当前节点的父节点
    @           选取属性
    *           匹配任何元素节点
    @*          匹配任何属性节点
    Node()      匹配任何类型的节点

#### CSS选择器

　　CSS层叠样式表，语法由两个主要部分组成：选择器，一条或多条声明
Selector {declaration1;declaration2;……}

**下面为常用的使用方法**

    .class              .color              选择class=”color”的所有元素
    #id                 #info               选择id=”info”的所有元素
    *                   *                   选择所有元素
    element             p                   选择所有的p元素
    element,element     div,p               选择所有div元素和所有p元素
    element element     div p               选择div标签内部的所有p元素
    [attribute]         [target]            选择带有targe属性的所有元素
    [arrtibute=value]   [target=_blank]     选择target=”_blank”的所有元素

#### 选择器的使用例子

　　上面我们列举了两种选择器的常用方法，下面通过scrapy帮助文档提供的一个地址来做演示
地址：[http://doc.scrapy.org/en/latest/_static/selectors-sample1.html](http://doc.scrapy.org/en/latest/_static/selectors-sample1.html)
这个地址的网页源码为：

    <html>
	<head>
	    <base href='http://example.com/'/>
	    <title>Example website</title>
	</head>
	<body>
	<div id='images'>
	    <a href='image1.html'>Name: My image 1 <br/><img src='image1_thumb.jpg'/></a>
	    <a href='image2.html'>Name: My image 2 <br/><img src='image2_thumb.jpg'/></a>
	    <a href='image3.html'>Name: My image 3 <br/><img src='image3_thumb.jpg'/></a>
	    <a href='image4.html'>Name: My image 4 <br/><img src='image4_thumb.jpg'/></a>
	    <a href='image5.html'>Name: My image 5 <br/><img src='image5_thumb.jpg'/></a>
	</div>
	</body>
	</html>

　　我们通过scrapy shell [http://doc.scrapy.org/en/latest/_static/selectors-sample1.html来演示两种选择器的功能](http://doc.scrapy.org/en/latest/_static/selectors-sample1.html%E6%9D%A5%E6%BC%94%E7%A4%BA%E4%B8%A4%E7%A7%8D%E9%80%89%E6%8B%A9%E5%99%A8%E7%9A%84%E5%8A%9F%E8%83%BD)

**获取title**

　　这里的extract_first()就可以获取title标签的文本内容,因为我们第一个通过xpath返回的结果是一个列表，所以我们通过extract()之后返回的也是一个列表，而extract_first()可以直接返回第一个值，extract_first()有一个参数default,例如：extract_first(default="")表示如果匹配不到返回一个空

    In [1]: response.xpath('//title/text()')
    Out[1]: [<Selector xpath='//title/text()' data='Example website'>]
    
    In [2]: response.xpath('//title/text()').extract_first()
    Out[2]: 'Example website'
    
    In [6]: response.xpath('//title/text()').extract()
    Out[6]: ['Example website']

　　同样的我们也可以通过css选择器获取，例子如下：

    In [7]: response.css('title::text')
    Out[7]: [<Selector xpath='descendant-or-self::title/text()' data='Example website'>]
    
    In [8]: response.css('title::text').extract_first()
    Out[8]: 'Example website'

**查找图片信息**  
　　这里通过xpath和css结合使用获取图片的src地址：

    In [13]: response.xpath('//div[@id="images"]').css('img')
    Out[13]: 
    [<Selector xpath='descendant-or-self::img' data='<img src="image1_thumb.jpg">'>,
     <Selector xpath='descendant-or-self::img' data='<img src="image2_thumb.jpg">'>,
     <Selector xpath='descendant-or-self::img' data='<img src="image3_thumb.jpg">'>,
     <Selector xpath='descendant-or-self::img' data='<img src="image4_thumb.jpg">'>,
     <Selector xpath='descendant-or-self::img' data='<img src="image5_thumb.jpg">'>]
    
    In [14]: response.xpath('//div[@id="images"]').css('img::attr(src)').extract()
    Out[14]: 
    ['image1_thumb.jpg',
     'image2_thumb.jpg',
     'image3_thumb.jpg',
     'image4_thumb.jpg',
     'image5_thumb.jpg']

**查找a标签信息**  
　　这里分别通过xapth和css选择器获取a标签的href内容，以及文本信息，css获取属性信息是通过attr,xpath是通过@属性名

    In [15]: response.xpath('//a/@href')
    Out[15]: 
    [<Selector xpath='//a/@href' data='image1.html'>,
     <Selector xpath='//a/@href' data='image2.html'>,
     <Selector xpath='//a/@href' data='image3.html'>,
     <Selector xpath='//a/@href' data='image4.html'>,
     <Selector xpath='//a/@href' data='image5.html'>]
    
    In [16]: response.xpath('//a/@href').extract()
    Out[16]: ['image1.html', 'image2.html', 'image3.html', 'image4.html', 'image5.html']
    
    In [17]: response.css('a::attr(href)')
    Out[17]: 
    [<Selector xpath='descendant-or-self::a/@href' data='image1.html'>,
     <Selector xpath='descendant-or-self::a/@href' data='image2.html'>,
     <Selector xpath='descendant-or-self::a/@href' data='image3.html'>,
     <Selector xpath='descendant-or-self::a/@href' data='image4.html'>,
     <Selector xpath='descendant-or-self::a/@href' data='image5.html'>]
    
    In [18]: response.css('a::attr(href)').extract()
    Out[18]: ['image1.html', 'image2.html', 'image3.html', 'image4.html', 'image5.html']
    
    In [27]: response.css('a::text').extract()
    Out[27]: 
    ['Name: My image 1 ',
     'Name: My image 2 ',
     'Name: My image 3 ',
     'Name: My image 4 ',
     'Name: My image 5 ']
    
    In [28]: response.xpath('//a/text()').extract()
    Out[28]: 
    ['Name: My image 1 ',
     'Name: My image 2 ',
     'Name: My image 3 ',
     'Name: My image 4 ',
     'Name: My image 5 ']
    
    In [29]: 

**高级用法**  
　　查找属性名称包含img的所有的超链接，通过contains实现

    In [36]: response.xpath('//a[contains(@href,"image")]/@href').extract()
    Out[36]: ['image1.html', 'image2.html', 'image3.html', 'image4.html', 'image5.html']
    
    In [37]: response.css('a[href*=image]::attr(href)').extract()
    Out[37]: ['image1.html', 'image2.html', 'image3.html', 'image4.html', 'image5.html']
    
    In [38]: 

　　查找img的src属性

    In [41]: response.xpath('//a[contains(@href,"image")]/img/@src').extract()
    Out[41]: 
    ['image1_thumb.jpg',
     'image2_thumb.jpg',
     'image3_thumb.jpg',
     'image4_thumb.jpg',
     'image5_thumb.jpg']
    
    In [42]: response.css('a[href*=image] img::attr(src)').extract()
    Out[42]: 
    ['image1_thumb.jpg',
     'image2_thumb.jpg',
     'image3_thumb.jpg',
     'image4_thumb.jpg',
     'image5_thumb.jpg']
    
    In [43]: 

　　提取a标签的文本中name后面的内容，这里提供了正则的方法re和re_first

    In [43]: response.css('a::text').re('Name\:(.*)')
    Out[43]: 
    [' My image 1 ',
     ' My image 2 ',
     ' My image 3 ',
     ' My image 4 ',
     ' My image 5 ']
    
    In [44]: response.css('a::text').re_first('Name\:(.*)')
    Out[44]: ' My image 1 '