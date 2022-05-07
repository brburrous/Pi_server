from flask import render_template, request, jsonify
from app import app



# ports = move.usb_id()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    print(request.data)
    try:
        json = request.json
        direction = json["direction"]
        move = json["move"] 
        return f"Cool beans", 200
    except Exception as e:
        return f"An Error Occured: {e}", 400

