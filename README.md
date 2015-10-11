# Hydra

Hydra是基于生产者-消费者模型的一个多进程任务引擎。
海德拉是希腊神话中的九头蛇怪，砍掉一个头，马上会再生出两个，最后被海格力斯所打败。
命名为海德拉的原因很简单，因为语言是python，有多个头的python，自然就是传说中的九头蛇啦。

### 特性

* 无第三方依赖库，轻量级
* 运行效率高，充分利用多核
* 简单易于上手

### 依赖

* python 2.7


### 运行环境

* windows
* ubuntu(其它*unix没有测试)

特别说明，**不支持**mac os x，因为使用到了multiprocessing模块中的queue，其中一个方法，qsize，mac os x并没有实现。

> qsize()
Return the approximate size of the queue. Because of multithreading/multiprocessing semantics, this number is not reliable.
Note that this may raise NotImplementedError on Unix platforms like Mac OS X where sem_getvalue() is not implemented.


### 安装

`git clone https://github.com/Hugh-wong/hydra.git`


### 如何应用

##### 定义一个取任务的函数

```python

def retrieve_items(need_count):
    pass

```

该函数从文件/数据库/缓存等取出来数据（注意如果开启多个hydra，则要注意保证一定的锁机制）。

取多少数据，由need_count指定，一般不超过给定的进程数。

##### 定义任务的执行函数

```python

def consume(item):
    pass

```

该函数从Broker（海德拉使用multiprocessing.Queue作为中介者）中取到item，然后消费该数据


##### 执行后的结果呢？

该结果通常由consume来实现，通常是写回到数据库/缓存中去。


### 例子

参考`test.py`，这个例子就是随机给几个数字，然后求素数之和。


### 其它特性 && 说明

一、任务时间控制，可以很方便控制任务执行时间。

二、支持多任务，可以根据机器硬件，配置几个不同的任务。

三、退出机制较完善，任务退出时，首先等待任务执行完毕后（或等待超时）时退出，全部任务都完毕后方可退出。


其它说明：

死循环问题，由于Manager写的是While True，这里可能会持续跑N天，但是特别要提出的一点是Mysql的不完善，在我所应用的项目中，超过8个小时，
mysql就会出现`mysql server has gone away`的问题，而mongodb则状态良好。

所以尽量不要使用mysql作任务存储，可以使用mongodb或者redis。实在不行，建议将死循环改成一定的时候，结合supervisor作自动重启也是可以的。


### 使用supervisor管理

supervisor是进程守护利器，自然可以管理hydra，这里要注意一下配置：

```
killasgroup = true
stopasgroup = true
stopwaitsecs=10
```



