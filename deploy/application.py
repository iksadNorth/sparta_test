from flask import Flask, render_template, request, jsonify
application = app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.3lyhcbq.mongodb.net/?retryWrites=true&w=majority', tlsAllowInvalidCertificates=True)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_give = request.form['bucket_give']

    bucket_list = list(db.bucket.find({}, {'_id': False}))
    count = len(bucket_list) + 1
    
    doc ={
        'num': count,
        'bucket': bucket_give,
        'done': 0,
    }
    
    db.bucket.insert_one(doc)
    return jsonify({'msg': '체크 리스트 추가 완료!'})

@app.route("/bucket/<int:num>", methods=["PATCH"])
def bucket_patch(num):
    db.bucket.update_one({'num': num}, {'$set': {'done': 1}})
    return jsonify({'msg': '체크 리스트 완료!'})
    
@app.route("/bucket", methods=["GET"])
def bucket_get():
    all_buckets = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'result': all_buckets})

if __name__ == '__main__':
    app.run()