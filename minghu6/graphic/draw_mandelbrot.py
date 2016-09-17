# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
################################################################################
global 1.g_size:graphic size
               (the more smaller of value the more bigger of the graphic size)
       2.param_dict: package parameter from control to worker function
       3.draw_func: which graphic func will gonna be called
################################################################################
"""

#encoding=utf-8
import numpy as np
import pylab as pl
import time
from matplotlib import cm
from math import log

from minghu6.algs.timeme import timeme

def draw_mandelbrot(C=0,power=1+5j,N=800,
                    cx=0,cy=0,d=2.5,escape_radius = 2,iter_num = 100):
    """
    绘制点(cx, cy)附近正负d的范围的Mandelbrot
    """

    with timeme() as t:
        x0, x1, y0, y1 = cx-d, cx+d, cy-d, cy+d
        y, x = np.ogrid[y0:y1:N*1j, x0:x1:N*1j]
        z0 = x + y*1j


        def smooth_iter_point(z0,c):


            z = z0 #赋初值

            for i in range(1, iter_num):
                if abs(z)>escape_radius: break
                z = z**power+c  # **运算符是幂运算
            #下面是重新计算迭代次数，可以获取连续的迭代次数（即正规化）

            absz = abs(z) #复数的模
            if absz > 2.0:
                mu = i - log(log(abs(z),2),2)
            else:
                mu = i

            return mu # 返回正规化的迭代次数

        smooth_mand = np.frompyfunc(smooth_iter_point,2,1)(z0,C).astype(np.float)

    print(t)
    pl.gca().set_axis_off()
    pl.imshow(smooth_mand,extent=[x0,x1,y1,y0])

    pl.show()



def draw_mandelbrot_2(cx, cy, d,degree=2, N=800):
    """
    与draw_mandelbrot相比，是不同的实现方法，搞不太懂，也能绘图，但不好定制
    绘制点(cx, cy)附近正负d的范围的Mandelbrot
    """

    with timeme() as t0:
        global mandelbrot

        x0, x1, y0, y1 = cx-d, cx+d, cy-d, cy+d
        y, x = np.ogrid[y0:y1:N*1j, x0:x1:N*1j]
        c = x+y*1j

        # 创建X,Y轴的坐标数组
        ix, iy = np.mgrid[0:N,0:N]

        # 创建保存mandelbrot图的二维数组，缺省值为最大迭代次数
        mandelbrot = np.ones(c.shape, dtype=np.int)*100

        # 将数组都变成一维的
        ix.shape = -1
        iy.shape = -1
        c.shape = -1
        z = c.copy() # 从c开始迭代，因此开始的迭代次数为1

        start = time.clock()

    with timeme() as t1:
        t1_1=0
        t1_2=0
        t1_3=0
        for i in range(1,100):
            # 进行一次迭代
            with timeme() as t:
                z = z**degree+c

            t1_1+=t.total
            # 找到所有结果逃逸了的点
            with timeme() as t:
                tmp = np.abs(z) > 2.0
                # 将这些逃逸点的迭代次数赋值给mandelbrot图
                mandelbrot[ix[tmp], iy[tmp]] = i

            t1_2+=t.total
            with timeme() as t:
                # 找到所有没有逃逸的点
                np.logical_not(tmp, tmp)
                # 更新ix, iy, c, z只包含没有逃逸的点
                ix,iy,c,z = ix[tmp], iy[tmp], c[tmp],z[tmp]
                len_z=len(z)
            t1_3+=t.total

            if len_z == 0: break

    with timeme() as  t2:
        print ("time=",time.clock() - start)

        pl.imshow(mandelbrot, cmap=cm.Blues_r, extent=[x0,x1,y1,y0])
        pl.gca().set_axis_off()

    all_t=t0.total+t1.total+t2.total
    print('t0:',t0,t0.total/all_t)
    print('t1:',t1,t1.total/all_t)
    print('t1_1',t1_1)
    print('t1_2',t1_2)
    print('t1_3',t1_3)
    print('t2:',t2,t2.total/all_t)
    pl.show()

################################################################################
#Use Parallel Architecture
################################################################################

def draw_mandelbrot_mpich(C=0,power=1+5j,N=800,
                          cx=0,cy=0,d=2.5,escape_radius = 2,iter_num = 100):
    """
    Use MPICH Parallel Architecture
    :param C:
    :param power:
    :param N:
    :param cx:
    :param cy:
    :param d:
    :param escape_radius:
    :param iter_num:
    :return:
    """
    global comm
    comm_rank=comm.Get_rank()
    comm_size=comm.Get_size()


    with timeme() as t:
        if comm_rank==0:
            x0, x1, y0, y1 = cx-d, cx+d, cy-d, cy+d
            y, x = np.ogrid[y0:y1:N*1j, x0:x1:N*1j]
            z0=x+y*1j
            #z0=z0.reshape(z0.size)

        else:
            z0=None

        z0=comm.bcast(z0,root=0)

        slice_size=N//comm_size
        extent_size=N-comm_size*slice_size

        if comm_rank==0:
            z0_self=z0[:slice_size+extent_size]
        else:
            start=slice_size*comm_rank+extent_size
            end=start+slice_size
            z0_self=z0[start:end]


        def smooth_iter_point(z0,c):


            z = z0 #赋初值

            for i in range(1, iter_num):
                if abs(z)>escape_radius: break
                z = z**power+c  # **运算符是幂运算
            #下面是重新计算迭代次数，可以获取连续的迭代次数（即正规化）


            absz = abs(z) #复数的模
            if absz > 2.0:
                mu = i - log(log(abs(z),2),2)
            else:
                mu = i

            return mu # 返回正规化的迭代次数

        smooth_mand_self = np.frompyfunc(smooth_iter_point,2,1)(z0_self,C).astype(np.float)

        smooth_mand_list=comm.allgather(smooth_mand_self)

        #print(type(smooth_mand_list),comm_rank)
        smooth_mand=np.vstack(smooth_mand_list)

    if comm_rank==0:
        pl.gca().set_axis_off()
        print(t)
        pl.imshow(smooth_mand,extent=[x0,x1,y1,y0])
        pl.show()


    pass



################################################################################
#Controller
################################################################################
def draw_MandelbrotSet(C=1+5j,power=2,N=800,
                       cx=0,cy=0,d=2.5,escape_radius = 2,
                       iter_num = 100):

    global g_size
    global param_dict
    global draw_func
    param_dict=locals()





    if draw_func==draw_mandelbrot_mpich:
        import mpi4py.MPI as MPI
        global comm
        comm=MPI.COMM_WORLD

    g_size= d


        #鼠标点击触发执行的函数
    def on_press(event):
        global g_size
        global param_dict
        print (event)
        print (dir(event))
        newx = event.xdata
        newy = event.ydata
        print ((newx,newy))

        #不合理的鼠标点击，直接返回，不绘制
        if newx == None or newy == None  or event.dblclick == True:
            return None
        #不合理的鼠标点击，直接返回，不绘制
        if event.button == 1:  #button ==1 代表鼠标左键按下， 是放大图像
            g_size /= 2
        elif event.button == 3: #button == 3 代表鼠标右键按下， 是缩小图像
            g_size *= 2
        else:
            return None
        print (g_size)

        param_dict['cx'],param_dict['cy']=newx,newy
        param_dict['d']=g_size
        draw_func(**param_dict)

    fig, ax = pl.subplots(1)
    #注册鼠标事件
    fig.dpi=25
    fig.canvas.mpl_connect('button_press_event', on_press)
    #初始绘制一个图
    draw_func(**param_dict)
def interactive():
    import argparse
    from ast import literal_eval as eval

    parser=argparse.ArgumentParser()


    parser.add_argument('-C','--C',type=eval,default=0,
                        help='z_k+1=z_k^power+C')

    parser.add_argument('-p','--power',type=eval,default=2,
                        help='z_k+1=z_k^power+C')

    parser.add_argument('-x','--x',dest='cx',type=int,default=0,
                        help='cx')

    parser.add_argument('-y','--y',dest='cy',type=int,default=0,
                        help='cy')

    parser.add_argument('-d','--d',type=eval,default=2.5,
                        help='(cx-d,cx+d) (cy-d,cy+d)')

    parser.add_argument('-e','--escape_radius',type=eval,default=2,
                        help=('Escape Radius,default 2 \n'
                              'Do not change'))

    parser.add_argument('-n','--iter_num',type=int,default=100,
                        help='Max number of iter times')


    parser.add_argument('-f','--func',dest='draw_func',
                        choices=['normal','mpich'],
                        help='select kind of exec,default(normal)')


    args=parser.parse_args()

    global draw_func
    if args.draw_func!=None:
        if args.draw_func == 'normal':
            draw_func=draw_mandelbrot
        elif args.draw_func=='mpich':
            draw_func=draw_mandelbrot_mpich
        else:
            raise Exception('args f error')
    else:
        draw_func=draw_mandelbrot

    from minghu6.algs.dict import remove_key,remove_value
    args=remove_value(remove_key(args.__dict__,'draw_func'),None)


    return args
if __name__ == '__main__':
    args=interactive()
    draw_MandelbrotSet(**args)