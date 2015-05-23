# Hydra
producer-consumer based python task engine


## When to use?

* when your backend task is too much, and want to done as soon as possible.

## Usage

    # define or import your retrieve_items and consume functions here

    from hydra.manager import Manager
    cfg_list = [{'retrieve_items':  retrieve_items, 'consume': consume_item, 'consumer_count':2, 'working_time': [('00:00', '23:59')]}]
    Manager.trigger(**cfg_list)

## How to define a retrieve_items fucntion?

* items are saved in db/mq or any broker.
* make sure do not get the duplicated items.(e.g. might use a global lock)

## how to define a consume function?

nothing special.

