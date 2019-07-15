from flask import Flask, jsonify, request
from uuid import uuid4
import cloudpickle, base64, _thread

uuid = lambda: str(uuid4())
b64e = lambda raw: base64.b64encode(raw)
b64d = lambda b64: base64.b64decode(b64)

def run_task(uid, code):
	tasks[uid] = "running"
	code = cloudpickle.loads(base64.b64decode(code))
	res = code()
	tasks[uid] = "complete"
	results[uid] = res

app = Flask(__name__)
tasks = {}
results = {}

@app.route("/run", methods=['GET','POST'])
def app_run():
	code = request.form['code'] if request.method == 'POST' else request.args['code']
	uid = uuid()
	_thread.start_new_thread(run_task, (uid, code))
	return uid
@app.route("/check/<uid>")
def app_check(uid):
	return tasks[uid] if uid in tasks else "not found"
@app.route("/get/<uid>")
def app_get(uid):
	return jsonify({'output':results[uid]}) if uid in results else "not found"

app.run(host="0.0.0.0", port=8080) if __name__ == "__main__" else (lambda: (lambda: None)())()

