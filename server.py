from model.data_utils import CoNLLDataset
from model.ner_model import NERModel
from model.config import Config
from flask import Flask, request
import json
import server_utils

app = Flask(__name__)
config = Config()
model = NERModel(config)
model.build()
model.restore_session(config.dir_model)

def main():
    app.run(debug=True)


@app.route('/parse', methods=['POST'])
def parse():
    data = request.get_data()
    sentence = server_utils.preprocess(data.strip().decode())
    prediction = model.predict(sentence)
    print(prediction)
    parsed = server_utils.parseLabels(sentence, prediction)
    to_print = server_utils.align_data({"input": sentence, "output": prediction})

    return json.dumps(parsed) + '\n'

if __name__ == '__main__':
   main()
