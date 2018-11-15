


from wordcloud import WordCloud
from PIL import Image
import jieba
import matplotlib.pyplot as plt
import numpy as np
# #加载用户自定义词典
f = open('./day08.txt','r')
text = f.read()
text = text.replace(",","")
text = text.replace("[]","")
text = text.replace(" ","")
text = text.replace('"',"")


 
w = jieba.cut(text)
wl_space_split = ",".join(w)
font = "./xindexingcao57.ttf"

cloud_mask = np.array(Image.open("./003.png"))
my_wordcloud = WordCloud(mask=cloud_mask,background_color="white",\
font_path = font,min_font_size=10,max_font_size=100,width=400).generate(wl_space_split)
 
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()
# max_words = 500, max_font_size=50,margin=2


#加载需要使用的类库
# from PIL import Image
# import numpy as np
# from wordcloud import WordCloud, ImageColorGenerator
# from matplotlib import pyplot as plt
# #加载背景图片
# cloud_mask = np.array(Image.open("./bc_img/heart.jpeg"))
# #忽略显示的词
# st=set(["东西","这是"])
# #生成wordcloud对象
# wc = WordCloud(background_color="white", 
#     mask=cloud_mask,
#     max_words=200,
#     font_path="./font/wb.ttf",
#     min_font_size=15,
#     max_font_size=50, 
#     width=400, 
#     stopwords=st)
# wc.generate(cloud_text)
# wc.to_file("pic.png")
# #Parameters
#  |  ----------
#  |  font_path : string
#  |       使用的字体库
#  |  width : int (default=400)
#  |      图片宽度
#  |  height : int (default=200)
#  |      图片高度
#  |  mask : nd-array or None (default=None)
#  |      图片背景参考形状  
#  |  scale : float (default=1)
#  |      图幅放大、缩小系数  
#  |  min_font_size : int (default=4)
#  |      最小的字符
#  |  min_font_size : int (default=4)
#  |      最大的字符
#  |  max_words : number (default=200)
#  |      最多显示的词数
#  |  stopwords : set of strings or None
#  |      不需要显示的词
#  |  background_color : color value (default="black")
#  |      背景颜色
# --------------------- 