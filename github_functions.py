import json
import os
import time
from os.path import join, dirname

from github import Github
from dotenv import load_dotenv
import threading
from database import redis_server


class Function:
    def __init__(self, redis_server):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.redis_server = redis_server
        self.pubsub = redis_server.pubsub()
        self.pubsub.subscribe("newuser")
        self.discard = False
        self.users = list()

    def get_all_users(self):
        self.users = list(self.redis_server.scan_iter())

    def get_count(self, username):
        g = Github()
        user = g.get_user(username)
        all_user = 0
        for repo in user.get_repos():
            all_user += repo.get_contributors().totalCount
        return all_user / user.get_repos().totalCount

    def get_continuous_count(self, username):
        while not self.discard:
            self.redis_server.set(username, self.get_count(username))
            self.redis_server.publish("data", json.dumps({"name": username, "count": self.get_count(username)}))
            time.sleep(40)

    def count_for_all(self):
        for user in self.users:
            threading.Thread(target=self.get_continuous_count, args=(user.decode(),)).start()

    def check_new(self):
        if self.discard is False:
            self.pubsub.subscribe("newuser")
            for i in self.pubsub.listen():
                if i['type'] == "message":
                    self.discard = True
                    self.pubsub.unsubscribe()
        self.discard = False
        threading.Thread(target=self.check_new).start()
        self.get_all_users()
        self.count_for_all()


func = Function(redis_server)
threading.Thread(target=func.check_new).start()
func.get_all_users()
func.count_for_all()