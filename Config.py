import json


class Config:
    def __init__(self):
        with open("config.json") as file:
            self.data = json.load(file)

    def __call__(self, param):
        return self.data.get(param)


config = Config()


if __name__ == "__main__":
    print(config("conn_str"))