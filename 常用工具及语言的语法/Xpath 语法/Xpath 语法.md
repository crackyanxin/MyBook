# [Python爬虫：Xpath语法笔记](https://www.cnblogs.com/MUMO/p/5732836.html)

#### 一、选取节点

常用的路劲表达式：

|表达式|描述|实例|解释|
|--------|--------|--------|--------|
|nodename|选取nodename节点的所有子节点|xpath(‘//div’)|选取了div节点的所有子节点|
|/|从根节点选取|xpath(‘/div’)|从根节点上选取div节点|
|//|选取所有的当前节点，不考虑他们的位置|xpath(‘//div’)|选取所有的div节点|
|.|选取当前节点|xpath(‘./div’)|选取当前节点下的div节点|
|..|选取当前节点的父节点|xpath(‘..’)|回到上一个节点|
|@|选取属性|xpath（’//@calss’）|选取所有的class属性|

#### 二、谓语

谓语被嵌在方括号内，用来查找某个特定的节点或包含某个制定的值的节点

实例：

|表达式|结果|
|--------|--------|
|xpath(‘/body/div[1]’)|选取body下的第一个div节点|
|xpath(‘/body/div[last()]’)|选取body下最后一个div节点|
|xpath(‘/body/div[last()-1]’)|选取body下倒数第二个div节点|
|xpath(‘/body/div[positon()<3]’)|选取body下前两个div节点|
|xpath(‘/body/div[@class]’)|选取body下带有class属性的div节点|
|xpath(‘/body/div[@class=”main”]’)|选取body下class属性为main的div节点|
|xpath(‘/body/div[price>35.00]’)|选取body下price元素值大于35的div节点|

#### 三、通配符

Xpath通过通配符来选取未知的XML元素

|表达式|结果|
|--------|--------|
|xpath（’/div/*’）|选取div下的所有子节点|
|xpath(‘/div[@*]’)|选取所有带属性的div节点|

#### 四、取多个路径

使用“|”运算符可以选取多个路径

|表达式|结果|
|--------|--------|
|xpath(‘//div|//table’)|选取所有的div和table节点|

#### 五、Xpath轴

轴可以定义相对于当前节点的节点集

|轴名称|表达式|描述|
|--------|--------|--------|
|ancestor|xpath(‘./ancestor::*’)|选取当前节点的所有先辈节点（父、祖父）|
|ancestor-or-self|xpath(‘./ancestor-or-self::*’)|选取当前节点的所有先辈节点以及节点本身|
|attribute|xpath(‘./attribute::*’)|选取当前节点的所有属性|
|child|xpath(‘./child::*’)|返回当前节点的所有子节点|
|descendant|xpath(‘./descendant::*’)|返回当前节点的所有后代节点（子节点、孙节点）|
|following|xpath(‘./following::*’)|选取文档中当前节点结束标签后的所有节点|
|following-sibing|xpath(‘./following-sibing::*’)|选取当前节点之后的兄弟节点|
|parent|xpath(‘./parent::*’)|选取当前节点的父节点|
|preceding|xpath(‘./preceding::*’)|选取文档中当前节点开始标签前的所有节点|

 

|preceding-sibling|xpath(‘./preceding-sibling::*’)|选取当前节点之前的兄弟节点|
|--------|--------|--------|
|self|xpath(‘./self::*’)|选取当前节点|

 

#### 六、功能函数

使用功能函数能够更好的进行模糊搜索

|函数|用法|解释|
|--------|--------|--------|
|starts-with|xpath(‘//div[starts-with(@id,”ma”)]‘)|选取id值以ma开头的div节点|
|contains|xpath(‘//div[contains(@id,”ma”)]‘)|选取id值包含ma的div节点|
|and|xpath(‘//div[contains(@id,”ma”) and contains(@id,”in”)]‘)|选取id值包含ma和in的div节点|
|text()|xpath(‘//div[contains(text(),”ma”)]‘)|选取节点文本包含ma的div节点|
| | | |

scrapy xpath文档：[http://doc.scrapy.org/en/0.14/topics/selectors.html](http://doc.scrapy.org/en/0.14/topics/selectors.html)
