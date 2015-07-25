# Hydra
Hydra is a producer-consumer based python task engine.
It's totally process-based, can run several processes the same time to boost speed.
But there are a few differences between the ParallelPython.

* Continual running  without stop
* Can be paused any time

Yes, it's more like the task engie, `celery`, but more lightweight.

## When to use ?

Tasks are in numbers, and want to be finished as soon as possible.


## How to use ?

#### define a GET method

Use your own `retrieve_items` method, to load tasks from files, DBs, caches or anywhere you want.
And if you run hydra on several machines, you'd better use some lock system to avoid load the same data.

#### define a RUN method

Use your own `consume` method, to run the task from the `retrieve_items`.

Check the `test.py` to see how to use this.


# 海德拉

海德拉，是基于生产者-消费者模型的一个任务引擎。

海德拉是希腊神话中的九头蛇怪，砍掉一个头，马上会再生出两个，最后被海格力斯所打败。
为什么命名为海德拉，是因为语言是python，如果每个进程算一个头的话，确实是多头的生物。在死掉一两个头也确实不会造成太大的影响。

### 详细介绍

>Item（商品）：

    商品是能被生产、获取、消费的类。

>Producer（生产者）:

    会产生item，每种item的生产者不一样。

>Repository（仓库）:

    item被生产的位置。

>Allocator（分配者）：

    从仓库一批items，并放在合适的中介者中。

>Broker（中介者）：

    存储少量item，提供给消费者来取的位置。

>Consumer(消费者)：

    从broker中取item，并消费item，并循环。


一个item从被生产、到被消费的流程见下表：

Item | Producer | Repository | Allocator | Broker | Consumer
----| ---| ---| ---| ---|---|
itemA | produce | db.table or collection | retrieve_items | set_to_broker | get_item-->consume
itemB |
itemC|
...|

可以看到，整体流程是这样的：

定义商品 --> 被生产  --> 存储在仓库（防止重复） --> 由分配者一次取一批（防止竞争） --> 存放在中介者中 --> 消费者自取（防止竞争） --> 消费

为什么要有Allocator与Broker，这是因为在现实中，通常由消费者从仓库中自己取item代价较大，会有较大的IO开销。


其中仓库与中介者，是其它的两种存储引擎，仓库一般是数据库，而中介者，通常是线/进程安全的队列。

由于生产者的生产时机跟业务相关，比如用户触发啊、定时驱动等，而商品的保存、消费、取多少跟仓库听存储方式、及业务相关，也不具备普适性。

因此海德拉只研究和处理剩下的`分配者`与`消费者`。

