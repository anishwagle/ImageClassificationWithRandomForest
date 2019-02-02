from PIL import Image
import math
class Image_Crop:
    def __init__(self,img,thres=150):
        self.gx = [[0 for x in range(3)] for y in range(3)]
        self.gx[0][0]=3
        self.gx[0][1]=0
        self.gx[0][2]=-3
        self.gx[1][0]=10
        self.gx[1][1]=0
        self.gx[1][2]=-10
        self.gx[2][0]=3
        self.gx[2][1]=0
        self.gx[2][2]=-3
        self.gy = [[0 for x in range(3)] for y in range(3)]
        self.gy[0][0]=3
        self.gy[0][1]=10
        self.gy[0][2]=3
        self.gy[1][0]=0
        self.gy[1][1]=0
        self.gy[1][2]=0
        self.gy[2][0]=-3
        self.gy[2][1]=-10
        self.gy[2][2]=-3
        self.image = Image.open(img)
        self.width,self.height=self.image.size
        self.threshold = thres
        self.min_width=100
        self.min_height=100
        self.max_width=0
        self.max_height=0
        self.path=img
    
    def Edge_detection(self):
        self.down_size()
        new_img=Image.new(self.image.mode, self.image.size)
        isLimited=False
        
        while (isLimited==False):
            
            self.min_width=100
            self.min_height=100
            self.max_width=0
            self.max_height=0
            for x in range(0, self.width):
                for y in range(0, self.height):
                    sum_x = self.kernal_sum(x,y,check="gx")
                    sum_y = self.kernal_sum(x,y,check="gy")
                    sum_xy = int((sum_x**2 + sum_y**2)**(1/2))
                    white=(255,255,255)
                    black=(0,0,0)
                    if sum_xy>self.threshold:
                        new_img.putpixel((x,y),black)
                    else:
                        if x<self.min_width:
                            self.min_width=x
                        if x>self.max_width:
                            self.max_width=x
                        if y<self.min_height:
                            self.min_height=y
                        if y>self.max_height:
                            self.max_height=y
                        new_img.putpixel((x,y),white)
                        isLimited = True
            self.threshold += 500
        self.threshold=150
        if self.max_width==self.min_width:
            self.max_width=self.width
        if self.max_height==self.max_height:
            self.max_height=self.height
        left = self.min_width
        top = self.min_height
        right = self.max_width
        bottom = self.max_height
        self.image=self.image.crop((left,top,right,bottom))
        self.width,self.height=self.image.size
       # self.image.show()
        #new_img.show()
        var_list=self.Cal_Variance()
        var_list.append(self.width)
        var_list.append(self.height)
        return var_list

    def kernal_sum(self,x,y,check):
        p=[0,0,0,0,0,0,0,0,0]
        sum = 0
        if check=='gx':
            if(x-1)<0 or (y-1)<0:
                p[0]=255
            else:
                p[0]= self.get_pixel(x-1,y-1)*self.gx[0][0]
            
            if(x-1)<0:
                p[1]=255
            else:
                p[1]= self.get_pixel(x-1,y-1)*self.gx[0][1]
                    
            if(x-1)<0 or (y+1)>self.height:
                p[2]=255
            else:
                p[2]= self.get_pixel(x-1,y-1)*self.gx[0][2]

            if(y-1)<0:
                p[3]=255
            else:
                p[3]= self.get_pixel(x-1,y-1)*self.gx[1][0]

            p[4]= self.get_pixel(x-1,y-1)*self.gx[1][1]
            
            if(y+1)>self.height:
                p[5]=255
            else:
                p[5]= self.get_pixel(x-1,y-1)*self.gx[1][2]

            if(x+1)>self.width or (y-1)<0:
                p[6]=255
            else:
                p[6]= self.get_pixel(x-1,y-1)*self.gx[2][0]

            if(x+1)>self.width:
                p[7]=255
            else:
                p[7]= self.get_pixel(x-1,y-1)*self.gx[2][1]
                    
            if(x+1)>self.width or (y+1)>self.height:
                p[8]=255
            else:
                p[8]= self.get_pixel(x-1,y-1)*self.gx[2][2]
                    
        else:
            if(x-1)<0 or (y-1)<0:
                p[0]=255
            else:
                p[0]= self.get_pixel(x-1,y-1)*self.gy[0][0]
            
            if(x-1)<0:
                p[1]=255
            else:
                p[1]= self.get_pixel(x-1,y-1)*self.gy[0][1]
                    
            if(x-1)<0 or (y+1)>self.height:
                p[2]=255
            else:
                p[2]= self.get_pixel(x-1,y-1)*self.gy[0][2]

            if(y-1)<0:
                p[3]=255
            else:
                p[3]= self.get_pixel(x-1,y-1)*self.gy[1][0]

            p[4]= self.get_pixel(x-1,y-1)*self.gy[1][1]
            
            if(y+1)>self.height:
                p[5]=255
            else:
                p[5]= self.get_pixel(x-1,y-1)*self.gy[1][2]

            if(x+1)>self.width or (y-1)<0:
                p[6]=255
            else:
                p[6]= self.get_pixel(x-1,y-1)*self.gy[2][0]

            if(x+1)>self.width:
                p[7]=255
            else:
                p[7]= self.get_pixel(x-1,y-1)*self.gy[2][1]
                    
            if(x+1)>self.width or (y+1)>self.height:
                p[8]=255
            else:
                p[8]= self.get_pixel(x-1,y-1)*self.gy[2][2]

        for i in range(9):
            sum +=abs(p[i])
        sum = sum / 9
        return sum

    def get_pixel(self,x,y):
        pixel=self.image.getpixel((x,y))
        pix = self.gray_convert(pixel)
        return pix

    def gray_convert(self,pixel):
        gray = (pixel[0]+pixel[1]+pixel[2])*(1/3)
        return gray
    
    def down_size(self):
        self.image = self.image.resize((1000,1000),Image.ANTIALIAS)
        self.width,self.height=self.image.size
        return
    def get_avrage(self,iteam_list):
        sum = 0
        count=0
        for i in iteam_list:
            sum +=i 
            count +=1
        avg=sum/count
        tem=[]
        tem.append(count)
        tem.append(sum)
        tem.append(avg)
        return tem

    def Cal_Variance(self):
        gray=[]
        sat=[]
        variances=[]
        entropy = 0
        for x in range(0,self.width):
            for y in range(0,self.height):
                gray.append(self.gray_convert(self.image.getpixel((x,y))))
                r=self.red_convert(self.image.getpixel((x,y)))+1
                g=self.green_convert(self.image.getpixel((x,y)))+3
                b=self.blue_convert(self.image.getpixel((x,y)))+1
                sat.append((max(r,g,b)-min(r,g,b))/(max(r,g,b)))
                entropy += int((self.gray_convert(self.image.getpixel((x,y))))*(math.log2(self.gray_convert(self.image.getpixel((x,y)))+1)))

        var_list_gray = self.get_avrage(gray)
        var_gray_last=0
        var_list_sat = self.get_avrage(sat)
        for x in range(0,self.width):
            for y in range(0,self.height):
                var_gray_last+=(self.gray_convert(self.image.getpixel((x,y)))-var_list_gray[2])**2
        last_gray=int(var_gray_last/(var_list_gray[0]-1))
        
        var_sat=int(var_list_sat[1])
        variances.append(last_gray)
        variances.append(var_sat)
        variances.append(entropy)
        return variances
    def red_convert(self,pixel):
        red = pixel[0]
        return red
    def green_convert(self,pixel):
        green = pixel[1]
        return green
    def blue_convert(self,pixel):
        blue = pixel[2]
        return blue