#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: consumer.py
@time: 2018/12/31 14:45:37
@desc:

"""

from channels.generic.websocket import AsyncWebsocketConsumer
import json


class DeployResult(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_group = self.scope["url_route"]["kwargs"]["group"]
        self.uid = self.scope["url_route"]["kwargs"]["uid"]
        # 收到连接时候处理，
        await self.channel_layer.group_add(
            self.chat_group,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 关闭channel时候处理
        await self.channel_layer.group_discard(
            self.chat_group,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # 发送消息到组
        await self.channel_layer.group_send(
            self.chat_group,
            {
                'type': 'client.message',
                'message': message
            }
        )

    # 处理客户端发来的消息
    async def client_message(self, event):
        message = event['message']
        # 发送消息到 WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


def start():
    pass


if __name__ == '__main__':
    start()
