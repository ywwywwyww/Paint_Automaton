from selenium import webdriver
from PIL import Image,ImageDraw
import numpy
import numpy.matlib
import websocket
import random
import math
import time



num=216

tot=256

def init_ws():
	global ws
	ws=websocket.WebSocket()
	ws.connect("ws://192.168.63.158:1919")

def post(x, y, r,g,b):
	global ws
	js = '%d|%d|%d|%d|%d' % (x, y, r,g,b)
	# print(js)
	ws.send(js)

def NO_to_RGB(x):
	r=x//(tot*tot)
	g=x//tot%tot
	b=x%tot
	return (r,g,b)
	# return (float(r)/(tot-1)*255,float(g)/(tot-1)*255,float(b)/(to-1)*255)

def RGB_to_NO(r,g,b):
	r=round(r)
	g=round(g)
	b=round(b)
	return r*256*256+g*256+b
	# _r=round(r/(255/5))
	# _g=round(g/(255/5))
	# _b=round(b/(255/5))
	# return r*36+g*6+b

def sqr(x):
	return x*x

def get(r,g,b):
	return RGB_to_NO(r,g,b)
	# _r=round(float(r)/255*5)
	# _g=round(float(g)/255*5)
	# _b=round(float(b)/255*5)
	# return RGB_to_NO(_r,_g,_b)
	# mi=1e10
	# res=0
	# for i in range(0,num):
	# 	_r,_g,_b=NO_to_RGB(i)
	# 	temp=sqr(_r-r)+sqr(_g-g)+sqr(_b-b)
	# 	if(temp<mi):
	# 		mi=temp
	# 		res=i
	# return res

def get_HSV(r,g,b):
	mi=1e10
	res=0
	h,s,v=RGB_to_HSV(r,g,b)
	for i in range(0,num):
		_r,_g,_b=NO_to_RGB(i)
		_h,_s,_v=RGB_to_HSV(_r,_g,_b)
		temp=sqr(min(abs((_h-h)/360),1-abs((_h-h)/360)))+sqr(_s-s)+sqr(_v-v)
		if(temp<mi):
			mi=temp
			res=i
	return res

def init_webdriver():
	global browser
	browser = webdriver.Chrome()
	browser.get('http://192.168.63.158/')

# def post(x,y,color):
# 	js='ws.send("%d|%d|%d");'%(x,y,color)
# 	print(js)
# 	browser.execute_script(js)


def HSV_to_RGB(h, s, v):
	_h = (h // 60)%6
	f = h / 60 - _h
	p = v * (1 - s)
	q = v * (1 - f * s)
	t = v * (1 - (1 - f) * s)
	
	v*=255
	p*=255
	q*=255
	t*=255
	
	if (_h == 0):
		return (v, t, p);
	if (_h == 1):
		return (q, v, p);
	if (_h == 2):
		return (p, v, t);
	if (_h == 3):
		return (p, q, v);
	if (_h == 4):
		return (t, p, v);
	if (_h == 5):
		return (v, p, q);
	
def RGB_to_HSV(r,g,b):
	r=r/float(255)
	g=g/float(255)
	b=b/float(255)
	mi=float(min(r,min(g,b)))
	ma=float(max(r,max(g,b)))
	if(ma==mi):
		h=0
	elif(ma==r and g>=b):
		h=60*(g-b)/(ma-mi)
	elif(ma==r and g<b):
		h=60*(g-b)/(ma-mi)+360
	elif(ma==g):
		h=60*(b-r)/(ma-mi)+120
	else:
		h=60*(r-g)/(ma-mi)+240
	if(ma==0):
		s=0
	else:
		s=1-mi/ma
	v=ma
	return (h,s,v)

def init_img():
	img=Image.open('img.png')
	# img.show()
	
	rgb_img=img.convert('RGB')
	
	# rgb_img.show()
	
	global H,W
	
	H,W=img.size
	
	# print(H,W)
	
	# r,g,b=rgb_img.getpixel((H-1,W-1))

	# print(r,g,b)
	
	global r,g,b
	global h,s,v
	r=numpy.empty([H,W])
	g=numpy.empty([H,W])
	b=numpy.empty([H,W])
	h=numpy.empty([H,W])
	s=numpy.empty([H,W])
	v=numpy.empty([H,W])
	
	for i in range(0,H):
		for j in range(0,W):
			r[i,j],g[i,j],b[i,j]=rgb_img.getpixel((i,j))
			h[i,j],s[i,j],v[i,j]=RGB_to_HSV(r[i,j],g[i,j],b[i,j])
			# print(i,j,h[i,j],s[i,j],v[i,j])
			# print(i,j,r[i,j],g[i,j],b[i,j])
			# print(i,j,HSV_to_RGB(h[i,j],s[i,j],v[i,j]))
	
	global r_back,g_back,b_back
	r_back=r.copy()
	g_back=g.copy()
	b_back=b.copy()
		
def modify_img():
	
	global r_back,g_back,b_back
	global r,g,b
	
	r=r_back.copy()
	g=g_back.copy()
	b=b_back.copy()
	
	# c=numpy.matlib.zeros([3,3])
	#
	# for i in range(0,3):
	# 	a=[]
	# 	for j in range(0,3):
	# 		a.append(random.random()/3)
	# 	c[i]=a
	#
	# # print(c)
	#
	# for i in range(0,H):
	# 	for j in range(0,W):
	# 		rgb=numpy.matlib.zeros([3,3])
	# 		rgb[0]=[r[i,j],g[i,j],b[i,j]]
	# 		# print(rgb)
	# 		rgb=numpy.matmul(rgb,c)
	# 		# print(rgb)
	# 		r[i,j],g[i,j],b[i,j]=(rgb.tolist())[0]
	# 		# print(r[i,j],g[i,j],b[i,j])
		
	avgv=0
	
	h_offset=random.random()*360
	s_offset=random.random()
	v_offset=random.random()
			
	for i in range(0,H):
		for j in range(0,W):
			h,s,v=RGB_to_HSV(r[i,j],g[i,j],b[i,j])
			h+=h_offset
			if(h>360):
				h-=360
			s+=s_offset
			if(s>1):
				s-=1
			v+=v_offset
			if(v>1):
				v-=1
			# v=min(1,v*1.5)
			# print(i,j,v)
			r[i,j],g[i,j],b[i,j]=HSV_to_RGB(h,s,v)
			avgv+=v
	
	avgv/=H*W
	
	print(avgv)
	
def modify_img_2():
	global r_back, g_back, b_back
	global r, g, b
	
	r = r_back.copy()
	g = g_back.copy()
	b = b_back.copy()

	h_offset=random.random()*360
	s_offset=random.random()
	v_offset=random.random()

	for i in range(0,H):
		for j in range(0,W):
			h,s,v=RGB_to_HSV(r[i,j],g[i,j],b[i,j])
			h+=float(i)/H*360+h_offset
			if(h>360):
				h-=360
			s+=float(j)/W*1+s_offset
			if(s>1):
				s-=1
			v+=float(i)/H+float(j)/W+v_offset
			if(v>1):
				v-=1
			# v=min(1,v*1.3)
			# print(i,j,v)
			r[i,j],g[i,j],b[i,j]=HSV_to_RGB(h,s,v)
		
def draw(x,y):
	# for i in range(0,100):
	# 	for j in range(0,100):
	# 		post(i,j,0)
	# for i in range(H):
	# 	for j in range(W):
	# 		post(i,j,get(r[i,j],g[i,j],b[i,j]))
	
	for j in range(0, W):
		for i in range(0,H):
			post(x+i,y+j,r[i,j],g[i,j],b[i,j])
			# post(x+i,y+j,0)
		
def random_draw(x,y):
	# for i in range(0,H):
	# 	for j in range(0,W):
	# 		post(i,j,0,0,0)
	
	# b=(0,0)
	a = numpy.zeros(H*W, dtype =  [('x','i4'), ('y', 'i4')])
	for i in range (0,H):
		for j in range (0,W):
			a[i*W+j]=(i,j)
			
	# a_list=list(a)
	#
	# random.shuffle(a_list)
	#
	# a=a_list
	
	# for i in range(0,H):
	# 	for j in range(0,W):
	# 		print(a[i*W+j])
	# 		print(a[i*W+j][0],a[i*W+j][1])
	
	# print(a.__len__())
	#
	for i in range(0,a.__len__()):
		j=random.randint(0,i)
		if(j!=i):
			(a[i][0],a[j][0])=(a[j][0],a[i][0])
			(a[i][1],a[j][1])=(a[j][1],a[i][1])

	
	for i in range (0,a.__len__()):
		# print(i)
		_x=a[i][0]
		_y=a[i][1]
		# print(_x,_y)
		post(x+_x,y+_y,r[_x,_y],g[_x,_y],b[_x,_y])

def draw_img2():
	img2 = Image.new('RGB', (H, W), (255, 255, 255))
	img2_draw=ImageDraw.Draw(img2)
	
	for i in range(0,H):
		for j in range(0,W):
			_r,_g,_b=NO_to_RGB(get(r[i,j],g[i,j],b[i,j]))
			# _r,_g,_b=NO_to_RGB(get_HSV(r[i,j],g[i,j],b[i,j]))
			print(i,j,r[i,j],g[i,j],b[i,j])
			print(i,j,_r,_g,_b)
			img2_draw.point((i,j),fill=(int(_r),int(_g),int(_b)))
			# img2_draw.point((i,j),fill=(int(r[i,j]),int(g[i,j]),int(b[i,j])))
	
	img2.save('img2.png','png')

def draw_circle(x,y,R,r,g,b):
	for i in range(0,1280):
		for j in range(0,720):
			if(sqr(i-x)+sqr(j-y)<=R):
				post(i,j,r,g,b)
				
def walk():
	x=1280/2
	y=720/2
	h,s,v=RGB_to_HSV(255,0,0)
	while(1):
		h+=random.random()*10
		r,g,b=HSV_to_RGB(h,s,v)
		print(h,s,v)
		draw_circle(x,y,100,r,g,b)
		x+=random.randint(0,4)-2
		y+=random.randint(0,4)-2
		time.sleep(0.2)
	
	
	
# for i in range(0,32):
	# print(NO_to_RGB(i))
	# NO_to_RGB(i)
	
# init_webdriver()

init_ws()

init_img()
#
# while(1):
# 	modify_img()
# 	draw(0,0)


# draw_img2()

# draw(0,0)

# while(1):
# 	x=random.randint(0,1280-1)
# 	y=random.randint(0,720-1)
# 	r=random.randint(0,255)
# 	g=random.randint(0,255)
# 	b=random.randint(0,255)
# 	# post(x,y,0,0,0)
# 	post(x,y,r,g,b)
	


# while(1):
# 	for i in range(0,int(math.ceil(1280/H))):
# 		for j in range(0,int(math.ceil(720/W))):
# 			modify_img()
# 			# random_draw(i*H,j*W)
# 			draw(i*H,j*W)
# 		time.sleep(1)
# 	time.sleep(10)

# while(1):
# 	draw(random.randint(0,1280-1),random.randint(0,720-1))

# while(1):
# 	modify_img()
# 	random_draw(random.randint(0,1280-1),random.randint(0,720-1))
# 	time.sleep(5)
	
# for i in range(0,1280):
# 	for j in range(0,720):
# 		post(i,j,random.randint(0,255),random.randint(0,255),random.randint(0,255))
# 		# post(i,j,255,255,255)

# random_draw(4*H,0)

# random_draw(0,0)

# browser.quit()

# a=numpy.zeros([1280,720],dtype=int)

# for i in range(0,1280):
# 	for j in range(0,720):
# 		if((i&j)==0):
# 			post(i,j,0,0,0)
# 		# else:
# 		# 	post(i,j,255,255,255)
# 	time.sleep(0.1)

walk()

ws.close()