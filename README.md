# py_socket_logging_demo
A demo for python logging in multiprocessor env.

## 背景
Python 的logging模块是线程安全的，同一个进程的不同线程网同一份日志中写没有问题。但是，如果是多进程的程序，且配置了日志滚动，不同进程往同一份日志中写的时候就会遇到某个进程切了日志，但其他进程依旧往原来的位置写的问题。

> Although logging is thread-safe, and logging to a single file from multiple threads in a single process is supported,
> logging to a single file from multiple processes is not supported,
> because there is no standard way to serialize access to a single file across multiple processes in Python.
> If you need to log to a single file from multiple processes,
> one way of doing this is to have all the processes log to a SocketHandler,
> and have a separate process which implements a socket server which reads from the socket and logs to file. 

参考：[Logging to a single file from multiple processes](https://docs.python.org/2/howto/logging-cookbook.html)

## 方案1
使用 [ConcurrentLogHandler](https://pypi.python.org/pypi/ConcurrentLogHandler/0.9.1)
BUT，这个方法不支持日志按时间切割文件...

## 方案2
修改TimedRotatingFileHandler中的逻辑缺陷，或者重写FileHandler类，见参考2

## 方案3
就如文档中所说，所有logger使用SocketHandler，单独起一个进程来接受这些日志并写到日志文件中。此代码要实现的。

### 基本结构
- main
    - processor_1(sender_1) 
    - processor_2(sender_2)
    - processor_3(sender_3)
    - processor_4(receiver)

主进程生成4个子进程，其中3个子进程同时向processor_4发送日志，processor_4负责将日志写到文件并按时切割文件

## 参考
- 1. [Logging Cookbook](https://docs.python.org/2/howto/logging-cookbook.html)
- 2. [python logging日志模块以及多进程日志](http://www.jianshu.com/p/d615bf01e37b)
- 3. [Sending and receiving logging events across a network](https://docs.python.org/2/howto/logging-cookbook.html#sending-and-receiving-logging-events-across-a-network)
