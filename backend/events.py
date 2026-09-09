"""进程内事件总线:SSE 推送通道的服务器侧(D-P1-7,单向 服务器→浏览器)。

EventBroker 用 threading.Lock 保护订阅列表;publish 把统一事件字典
序列化为 SSE data 行广播给全部订阅者(单机单用户,广播是正确语义)。
"""

import json
import queue
import threading


class EventBroker:
    """注册/注销/广播 的最小事件总线。"""

    def __init__(self):
        self._lock = threading.Lock()
        self._subscribers: list[queue.Queue] = []

    def register(self) -> queue.Queue:
        """新订阅者:返回一个事件队列(SSE 端点消费它)。"""
        q: queue.Queue = queue.Queue(maxsize=500)
        with self._lock:
            self._subscribers.append(q)
        return q

    def unregister(self, q: queue.Queue) -> None:
        with self._lock:
            if q in self._subscribers:
                self._subscribers.remove(q)

    def publish(self, event: dict) -> None:
        """广播一条统一事件到所有订阅者;单个订阅者队列满则丢最旧(直播优先)。"""
        with self._lock:
            subscribers = list(self._subscribers)
        payload = json.dumps(event, ensure_ascii=False)
        for q in subscribers:
            try:
                q.put_nowait(payload)
            except queue.Full:
                try:
                    q.get_nowait()  # 丢最旧,保直播不阻塞
                    q.put_nowait(payload)
                except (queue.Empty, queue.Full):
                    pass


# 全局单例:main.py 与后台调用线程共享
broker = EventBroker()
