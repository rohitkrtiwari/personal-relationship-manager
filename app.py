# from flask import Flask, request, jsonify, abort
# from datetime import datetime
# from firebase_config import db

# app = Flask(__name__)

# @app.route('/posts', methods=['POST'])
# def create_post():
#     data = request.get_json()
#     post_ref = db.collection('posts').document()
#     post_ref.set({
#         'title': data['title'],
#         'content': data['content'],
#         'tags': data.get('tags', []),
#         'createdAt': datetime.now(),
#         'updatedAt': datetime.now()
#     })
#     return jsonify({"id": post_ref.id, "success": True}), 201

# @app.route('/posts', methods=['GET'])
# def get_posts():
#     posts = []
#     docs = db.collection('posts').order_by('createdAt', direction='DESCENDING').stream()
#     for doc in docs:
#         posts.append({"id": doc.id, **doc.to_dict()})
#     return jsonify(posts), 200


# @app.route('/posts/<post_id>', methods=['PUT'])
# def update_post(post_id):
#     data = request.get_json()
#     post_ref = db.collection('posts').document(post_id)
#     post_ref.update({
#         'title': data['title'],
#         'content': data['content'],
#         'tags': data.get('tags', []),
#         'updatedAt': datetime.now()
#     })
#     return jsonify({"success": True}), 200


# @app.route('/posts/<post_id>', methods=['DELETE'])
# def delete_post(post_id):
#     db.collection('posts').document(post_id).delete()
#     return jsonify({"success": True}), 200


# def validate_post_data(data):
#     if not data.get('title') or not data.get('content'):
#         abort(400, "Title and content are required")


# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({"error": "Resource not found"}), 404

# @app.errorhandler(500)
# def server_error(error):
#     return jsonify({"error": "Internal server error"}), 500


from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("search.html")  # simple HTML w/ search bar

if __name__ == "__main__":
    app.run(debug=True, port=5000)
